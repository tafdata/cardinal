import logging
import numpy as np
from datetime import datetime
import io
import openpyxl

from django.forms import formset_factory, modelformset_factory, BaseFormSet
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.utils import timezone # datetimeのwrapper
#from django.core.exceptions import DoesNotExist
from django.db.models.aggregates import Count

from competitions.models import Comp, Event, EventStatus

from organizer.models import Entry
from organizer.forms import SelectCompForm, EntryFilterForm, EntryForm, SLEditForm, EntryUploadFileForm

from organizer.upload import EntryHandler
from organizer.myprogram import ProgramMaker




# Create your views here.
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


# ================================ #
#   Index
# ================================ #
class OrganizerIndex(ListView):
    context_object_name = "comps"
    template_name = "organizer/index.html"
    paginated_by = 20

    def get(self, request, *args, **kwargs):
        self.object_list = Comp.objects.all().order_by('date')
        try:
            comp_code = request.session["comp_code"]
            comp = get_object_or_404(Comp, pk=comp_code)
            context =  self.get_context_data(object_list=self.object_list,comp_selected=comp)
            return self.render_to_response(context)
        except KeyError:        # 大会選択なし
            context =  self.get_context_data(object_list=self.object_list)
            return self.render_to_response(context)
        

def select_comp(request, comp_code):
    comp = get_object_or_404(Comp, pk=comp_code)
    
    if request.method == 'POST':
        form = SelectCompForm(request.POST, comp_code=comp.code)
        if form.is_valid():
            request.session["comp_code"] = comp.code
            return redirect('organizer:index')    
    else:
        form = SelectCompForm(comp_code=comp.code)
    return render(request,
                  'organizer/select_comp.html',
                  {"form": form, "comp": comp,})




# ================================ #
#   Entry
# ================================ #
class EntryList(ListView):
    context_object_name = "entries"
    template_name = "organizer/entry_list.html"
    paginated_by = 50

    def get(self, request, *args, **kwargs):
        try:
            comp = get_object_or_404(Comp, pk=request.session["comp_code"])
        except KeyError:
            return redirect('organizer:index')    

        if request.method == 'GET':
            # 絞り込みあり
            event_status = EventStatus.objects.filter(comp=comp).order_by('event')
            if "event" in request.GET:
                event = get_object_or_404(Event, pk=request.GET.get("event"))
                event_status = event_status.filter(event=event)
            if "section" in request.GET:
                event_status = event_status.filter(section=request.GET.get("section"))
                                        
            self.object_list =  Entry.objects.filter(event_status__in=event_status).order_by('event_status')
        else:
            # 絞り込みなし
            event_status = EventStatus.objects.filter(comp=comp).order_by('event')
            self.object_list =  Entry.objects.filter(event_status__in=event_status).order_by('event_status')
            
        form = EntryFilterForm(comp=comp)
        context = self.get_context_data(object_list=self.object_list, comp=comp, form=form)
        return self.render_to_response(context)

"""
エントリー追加 [個別]
"""
def check_entry(entry):
    # 性別の確認
    if not entry.sex == entry.event_status.event.sex:
        msg = "選択した種目と入力した性別が一致しません。"
        return False, msg
    return True, None


def entry_add(request):
    try:
        comp = get_object_or_404(Comp, pk=request.session["comp_code"])
    except KeyError:
        return redirect('organizer:index')
    msg = False
    
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            flg, msg = check_entry(new_entry)
            if flg:
                new_entry.entry_status = 'Entry'
                new_entry.save()
                return redirect('organizer:entry_list')
    else:
        form = EntryForm()

    return render(request,
                  'organizer/entry_add.html',
                  {'form': form, 'comp': comp, 'msg': msg})

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
                          'organizer/entry_add_by_file_error_check.html',
                          {'comp': comp, 'summary': summary, 'errors': errors})
    else:
        form = EntryUploadFileForm()

    return render(request,
                  'organizer/entry_add_by_file.html',
                  {'form': form, 'comp': comp})    
        


# ================================ #
#   SL | Start List
# ================================ #
def sl_top(request, event_status_id=None):
    try:
        comp = get_object_or_404(Comp, pk=request.session["comp_code"])
    except KeyError:
        return redirect('organizer:index')

    if event_status_id:
        # 種目が指定されていればその一覧を表示
        event_status = get_object_or_404(EventStatus, pk=event_status_id)
        entries = Entry.objects.filter(event_status=event_status).order_by('group', 'order_lane')
        return render(request,
                      'organizer/SL.html',
                      {'mode': "entry", 'comp': comp, 'event_status': event_status, 'entries': entries})
    else:
        # 種目が指定されていない場合は実施種目一覧を表示
        event_statuss = EventStatus.objects.filter(comp=comp)
        event_ids = event_statuss.values_list('event', flat=True).order_by('event').distinct()
        events = Event.objects.filter(id__in=event_ids).order_by('name')
        # 種目別スタートリストを出力可能か判定
        event_list = []
        for event in events:
            event_statuss_2 = EventStatus.objects.filter(comp=comp, event=event)
            flg = True
            for event_status in event_statuss_2:
                if event_status.start_list == False: flg = False
            event_list.append({'event': event, 'SL': flg})
            
        return render(request,
                      'organizer/SL.html',
                      {'mode': "event", 'comp': comp, 'event_statuss': event_statuss, 'event_list': event_list})
    
"""
SL 組,レーン試技順　編集ページ
"""
def sl_edit(request, event_status_id):
    try:
        comp = get_object_or_404(Comp, pk=request.session["comp_code"])
    except KeyError:
        return redirect('organizer:index')
    event_status = get_object_or_404(EventStatus, pk=event_status_id)
    entries = Entry.objects.filter(event_status=event_status).order_by('personal_best')
    SLEditFormSet = modelformset_factory(Entry,form=SLEditForm,extra=0)
    msg = False
    
    if request.method == 'POST':
        formset = SLEditFormSet(request.POST)
        if formset.is_valid():
            formset.save(commit=True)
            return redirect('organizer:sl_top', event_status_id=event_status.id)
        else:
            msg="入力内容に不備があります。入力内容を確認し直してください。"
            print(msg)
    else:
        formset = SLEditFormSet(queryset=entries)        

    return render(request,
                  'organizer/SL_edit.html',
                  {'formset': formset, 'comp': comp, 'event_status': event_status, 'msg': msg})    


"""
SL スタートリスト web表示
"""
def sl_web(request, event_status_id):
    try:
        comp = get_object_or_404(Comp, pk=request.session["comp_code"])
    except KeyError:
        return redirect('organizer:index')
    event_status = get_object_or_404(EventStatus, pk=event_status_id)

    # 組数を取得
    groups = Entry.objects.filter(event_status=event_status).values('group').annotate(cnt=Count("*"),)
    for group in groups:
        group["entries"] = Entry.objects.filter(event_status=event_status, group=group["group"]).order_by('order_lane')    
    # print("Groups: ",groups)

    return render(request,
                  'organizer/SL_web.html',
                  {'comp': comp, 'event_status': event_status, 'groups':groups})


"""
SL スタートリスト Excelダウンロード
"""
def sl_excel(request, sl_type=None, pk=None):
    comp = get_comp(request)
    PM = ProgramMaker(comp)
    
    # ダウンロード
    # Excel 作成
    if sl_type == "event":
        event = get_object_or_404(Event, pk=pk)
        wb = PM.cardinal_create_workbook_by_event(comp, event)
    elif sl_type == "event_status":
        event_status = get_object_or_404(EventStatus, pk=pk)
        event = event_status.event
        wb = PM.cardinal_create_workbook_by_event_status(comp, event_status)
    # 保存
    output = io.BytesIO()
    wb.save(output)
    # Response
    response = HttpResponse(output.getvalue(), content_type="application/excel")
    response["Content-Disposition"] = "filename="+event.sex+event.name+".xlsx"
    return response
