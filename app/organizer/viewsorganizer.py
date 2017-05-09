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
def entry_add(request, entry_method, event_status_id=None):
    # Params
    # - entry_method: 通常=entry, 当日=entry2
    comp = get_comp(request)
    msg = False
    
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            flg, msg = check_entry(new_entry)
            if flg:
                if entry_method == 'entry': new_entry.entry_status = 'Entry'
                else: new_entry.entry_status = 'Entry_2'
                new_entry.save()
                return redirect('organizer:organizer_top')
    else:
        if event_status_id:
            event_status = get_object_or_404(EventStatus, pk=event_status_id)
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

    
