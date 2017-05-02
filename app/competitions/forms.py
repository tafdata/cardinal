from django import forms
from competitions.models  import EventStatus
from competitions.models  import COMP_STATUS_CHOICES

#
# Form
#


#
# Status Update form
#
class EventStatusUpdateForm(forms.ModelForm):
    event_name = forms.CharField(
        widget=forms.HiddenInput())
    event_sex = forms.CharField(
        widget=forms.HiddenInput())
    
    class Meta:
        model = EventStatus
        fields = ['id', 'status',  'section']
        widgets = {
            'id': forms.HiddenInput(),            
            'section': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        event_status = kwargs['instance']
        super(EventStatusUpdateForm, self).__init__(*args, **kwargs)
        self.fields['event_name'].initial = event_status.event.name
        self.fields['event_sex'].initial = event_status.event.sex        
        self.fields['status'].widget.attrs.update({'class' : 'form-control form-control-sm'})



