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
from organizer.forms import DNSForm, EntryForm


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
def top(request):
    comp = get_comp(request)
    print(comp)
    
    return render(request,'organizer/guest/index.html',{'comp': comp})


        
"""
SL スタートリスト web版
"""
@login_required
def SL_web(request, event_status_id):
    comp = get_comp(request)
    event_status = get_object_or_404(EventStatus, pk=event_status_id)
    
    return render(request,
                  'organizer/guest/SL_web.html',
                  {'comp': comp, 'event_status': event_status})

"""
DNS
"""
@login_required
def DNS(request, entry_id):
    comp = get_comp(request)
    entry = get_object_or_404(Entry, pk=entry_id)
    event_status = entry.event_status
    
    if request.method == 'POST':
        form = DNSForm(request.POST, instance=entry)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.entry_status = 'DNS'
            entry.save()
            return redirect('organizer:guest_SL_web', event_status_id=event_status.id)
    else:
        form = DNSForm(instance=entry)
    return render(request,
                  'organizer/guest/DNS.html',
                  {'form': form, 'comp': comp, 'entry': entry, 'event_status': event_status})
    



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
def entry_add(request, event_status_id):
    comp = get_comp(request)
    event_status = get_object_or_404(EventStatus, pk=event_status_id)
    msg = False
    
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            flg, msg = check_entry(new_entry)
            if flg:
                new_entry.entry_status = 'Entry_2'
                new_entry.save()
                return redirect('organizer:guest_top')

            
    submit_url = reverse("organizer:guest_entry_add", kwargs={'event_status_id': event_status.id})
    return render(request,
                  'organizer/guest/entry_add.html',
                  {'comp': comp,'event_status': event_status, 'msg': msg, 'submit_url': submit_url})
