import logging
import numpy as np
from datetime import datetime
import io
import openpyxl

from django.forms import formset_factory, modelformset_factory, BaseFormSet
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.utils import timezone # datetimeのwrapper
#from django.core.exceptions import DoesNotExist
from django.db.models.aggregates import Count
from django.contrib.auth.decorators import login_required, user_passes_test

from competitions.models import Comp, Event, EventStatus

from organizer.models import Entry
from organizer.forms import SelectCompForm, EntryFilterForm, EntryForm, SLEditForm, EntryUploadFileForm, EntryStatusEditForm, SLUpdateForm

from organizer.upload import EntryHandler
from organizer.myprogram import ProgramMaker
from organizer.jyoriku import JyorikuTool


# ================================ #
#   Functions
# ================================ #
"""
セッション変数から運営中競技会のCompオブジェクトを取得
"""
def get_comp(request):
    try:
        return get_object_or_404(Comp, pk=request.session["comp_code"])
    except KeyError:
        return redirect('organizer:index')



# ===================
# 
#   運営責任者ページ
#
#====================
"""
TOP
"""
@login_required
@user_passes_test(lambda user: user.groups.filter(name='reception').exists())
def top(request):
    comp = get_comp(request)
    
    return render(request,'organizer/organizer/index.html',{'comp': comp})


"""
Entry 個別登録
"""
def check_entry(entry):
    # 性別の確認
    if not entry.sex == entry.event_status.event.sex:
        msg = "選択した種目と入力した性別が一致しません。"
        return False, msg
    return True, None


@login_required
@user_passes_test(lambda user: user.groups.filter(name='reception').exists())
def entry_add(request, entry_method, id=None):
    # Params
    # - entry_method: 通常=entry, 当日=entry2, edit=修正
    comp = get_comp(request)
    msg = False

    # POST
    if request.method == 'POST':
        if entry_method == 'edit':
            entry = get_object_or_404(Entry, pk=id)
            form = EntryForm(request.POST, instance=entry)
        else:
            form = EntryForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            flg, msg = check_entry(new_entry)
            if flg:
                if entry_method == 'entry': new_entry.entry_status = 'Entry'
                elif entry_method == 'entry2':
                    new_entry.entry_status = 'Entry_2'
                    new_entry.check = True
                new_entry.save()
                if entry_method == 'edit':
                    return redirect('organizer:organizer_SL_web', event_status_id=entry.event_status.id)
                else:
                    return redirect('organizer:organizer_top')
            
    # 修正
    if entry_method == 'edit':
        entry = get_object_or_404(Entry, pk=id)
        submit_url = reverse("organizer:organizer_entry_add", kwargs={'entry_method': entry_method, 'id': id})
        return render(request,
                      'organizer/organizer/entry_add.html',
                      {'comp': comp,'entry':entry, 'msg': msg, 'submit_url': submit_url})

    # 追加
    if id:
        event_status = get_object_or_404(EventStatus, pk=id)
    else:
        event_status = None
        submit_url = reverse("organizer:organizer_entry_add", kwargs={'entry_method': entry_method})
    return render(request,
                  'organizer/organizer/entry_add.html',
                  {'comp': comp,'event_status':event_status, 'msg': msg, 'submit_url': submit_url})


@login_required
@user_passes_test(lambda user: user.groups.filter(name='reception').exists())
def entry_add_by_file(request):
    comp = get_comp(request)
    
    if request.method == "POST":
        form = EntryUploadFileForm(request.POST, request.FILES)
        
        if form.is_valid():
            EH = EntryHandler(comp,form.cleaned_data["entry_status"])
            errors = EH.handle_csv(request.FILES['file'])
            summary = {
                "file_name": str(request.FILES['file']),
                "input_num": EH.success_num+len(EH.errors),
                "success_num": EH.success_num,
                "error_num": len(EH.errors)
            }
                
            return render(request,
                          'organizer/organizer/entry_add_by_file_check.html',
                          {'comp': comp, 'summary': summary, 'errors': errors})
    else:
        form = EntryUploadFileForm()

    return render(request,
                  'organizer/organizer/entry_add_by_file.html',
                  {'form': form, 'comp': comp}) 




"""
SL スタートリスト web版
"""
@login_required
@user_passes_test(lambda user: user.groups.filter(name='reception').exists())
def SL_web(request, event_status_id):
    comp = get_comp(request)
    event_status = get_object_or_404(EventStatus, pk=event_status_id)
    
    return render(request,
                  'organizer/organizer/SL_web.html',
                  {'comp': comp, 'event_status': event_status})



"""
SL 組,レーン試技順　編集ページ
"""
@login_required
@user_passes_test(lambda user: user.groups.filter(name='reception').exists())
def SL_edit(request, event_status_id):
    comp = get_comp(request)
    event_status = get_object_or_404(EventStatus, pk=event_status_id)
    entries = Entry.objects.filter(event_status=event_status).order_by('group', 'order_lane', 'personal_best')
    SLEditFormSet = modelformset_factory(Entry,form=SLEditForm,extra=0)
    msg = False
    
    if request.method == 'POST':
        formset = SLEditFormSet(request.POST)
        if formset.is_valid():
            formset.save(commit=True)
            return redirect('organizer:organizer_SL_web', event_status_id=event_status.id)
        else:
            msg="入力内容に不備があります。入力内容を確認し直してください。"
            print(msg)
    else:
        formset = SLEditFormSet(queryset=entries)        

    return render(request,
                  'organizer/organizer/SL_edit.html',
                  {'formset': formset, 'comp': comp, 'event_status': event_status, 'msg': msg})    



@login_required
@user_passes_test(lambda user: user.groups.filter(name='reception').exists())
def SL_update(request, event_status_id):
    comp = get_comp(request)
    event_status = get_object_or_404(EventStatus, pk=event_status_id)
    
    if request.method == 'POST':
        form = SLUpdateForm(request.POST, instance=event_status)
        if form.is_valid():
            form.save(commit=True)
            return redirect('organizer:organizer_top')
    else:
        form = SLUpdateForm(instance=event_status)   

    return render(request,
                  'organizer/organizer/SL_update.html',
                  {'form': form, 'comp': comp, 'event_status': event_status})    

    


"""
SL スタートリスト Excelダウンロード
"""
def SL_excel(request, sl_type=None, pk=None):
    comp = get_comp(request)
    PM = ProgramMaker(comp)
    
    # ダウンロード
    # Excel 作成
    if sl_type == "event":
        event = get_object_or_404(Event, pk=pk)
        wb = PM.cardinal_create_workbook_by_event(comp, event)
        if event.short:
            filename = str(event.sex)+str(event.short)+".xlsx"
        else:
            filename = str(event.sex)+str(event.name)+".xlsx"
        print(filename)
    elif sl_type == "event_status":
        event_status = get_object_or_404(EventStatus, pk=pk)
        event = event_status.event
        wb = PM.cardinal_create_workbook_by_event_status(comp, event_status)
        filename = str(event_status.section+event.sex+event.name+".xlsx")
    elif sl_type == "track":
        wb = PM.cardinal_create_workbook_track(comp=comp, mode='single')
        filename = "Track.xlsx"
    elif sl_type == "track2":
        wb = PM.cardinal_create_workbook_track(comp, mode='multiple')
        filename = "Track.xlsx"        
    elif sl_type == "field":
        wb = PM.cardinal_create_workbook_field(comp)
        filename = "Field.xlsx"
    else:
        return redirect('organizer:organizer_top')
    
    # 保存
    output = io.BytesIO()
    wb.save(output)
    # Response
    response = HttpResponse(output.getvalue(), content_type="application/excel")
    response["Content-Disposition"] = "filename="+filename
    return response


"""
SL スタートリスト 上陸用
"""
def SL_jyoriku(request):
    comp = get_comp(request)
    Jyoriku = JyorikuTool(comp)
    df = Jyoriku.start_list_jyoriku()
    
    # Response             
    response = HttpResponse(df.to_csv(header=False,index=False, encoding='utf-8'), content_type="text/csv")
    response["Content-Disposition"] = "filename='SL_cardinal_jyoriku.csv"
    return response    


def SL_cardinal(request):
    comp = get_comp(request)
    Jyoriku = JyorikuTool(comp)
    df = Jyoriku.start_list_cardinal()
    
    # Response             
    response = HttpResponse(df.to_csv(index=False, encoding='utf-8'), content_type="text/csv")
    response["Content-Disposition"] = "filename='cardinal_SL.csv"
    return response    
