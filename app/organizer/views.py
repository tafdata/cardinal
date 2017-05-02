import logging
import numpy as np
from datetime import datetime

from django.forms import formset_factory, modelformset_factory, BaseFormSet
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.utils import timezone # datetimeのwrapper
#from django.core.exceptions import DoesNotExist

from competitions.models import Comp, Event, EventStatus

from organizer.models import Entry
from organizer.forms import SelectCompForm, EntryFilterForm, EntryForm



# Create your views here.
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
