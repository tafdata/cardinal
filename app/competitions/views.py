import logging
import numpy as np
from datetime import datetime

from django.forms import formset_factory, modelformset_factory, BaseFormSet
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.utils import timezone # datetimeのwrapper


from competitions.models import Comp, Event, EventStatus
from competitions.forms  import EventStatusUpdateForm



# Create your views here.

# ================================ #
#   Index
# ================================ #
def index(request):
    return render(request,
                  'competitions/index.html')

# ================================ #
#   Comp 一覧
# ================================ #
class CompList(ListView):
    context_object_name = "comps"
    template_name = 'competitions/comp_list.html'
    paginated_by = 20

    def get(self, request, *args, **kwargs):
        self.object_list = Comp.objects.all().order_by('date')

        context = self.get_context_data(object_list=self.object_list)
        return self.render_to_response(context)

    
    
# ================================ #
#   Event 一覧
# ================================ #
class EventList(ListView):
    context_object_name = "events"
    template_name = 'competitions/event_list.html'
    paginated_by = 20

    def get(self, request, *args, **kwargs):
        self.object_list = Event.objects.all().order_by('name')

        context = self.get_context_data(object_list=self.object_list)
        return self.render_to_response(context)


# ================================ #
#   EventStauts | Compを指定
# ================================ #
class EventStatusList(ListView):
    context_object_name = "statuss"
    template_name = 'competitions/event_status_list.html'
    paginated_by = 20

    def get(self, request, *args, **kwargs):
        comp = get_object_or_404(Comp, pk=kwargs["comp_code"])        
        self.object_list = EventStatus.objects.filter(comp=comp).order_by('event')

        context = self.get_context_data(object_list=self.object_list, comp=comp)
        return self.render_to_response(context)

    
#
# Event Status Update
#        
def update_event_status(request, comp_code):
    comp = get_object_or_404(Comp, pk=comp_code)
    event_statuss = EventStatus.objects.filter(comp=comp).order_by('event')
    EventStatusFormSet = modelformset_factory(EventStatus,
                                               form=EventStatusUpdateForm,
                                               extra=0)    
    if request.method == 'POST':
        formset = EventStatusFormSet(request.POST)
        if formset.is_valid():
            formset.save()
        else:
            print("invalid")
        return redirect('competitions:event_status_list', comp_code=comp.code)
    else:
        formset = EventStatusFormSet(queryset=event_statuss)        
    return render(request,
                  'competitions/event_status_update.html',
                  {'formset': formset, 'comp': comp})


def update_event_status_single(request, event_status_id):
    event_status = get_object_or_404(EventStatus, pk=event_status_id)
    
    if request.method == 'POST':
        form = EventStatusUpdateForm(request.POST, instance=event_status)
        if form.is_valid():
            form.save(commit=True)
        else:
            print("invalid")
        return redirect('competitions:event_status_list', comp_code=event_status.comp.code)
    else:
        form = EventStatusUpdateForm(instance=event_status)
    return render(request,
                  'competitions/event_status_update_single.html',
                  {'form': form, 'event_status': event_status})    
