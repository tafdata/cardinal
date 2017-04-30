from django import forms
from competitions.models  import EventStatus, STATUS_CHOICES

#
# Form
#


#################################################
# 
#   BaseFormsetのオーバーライド
#   ==> formsetのindexを各フォームのkwargsに追加
#
class AddFormIndexIntoKwargsFormSet(forms.BaseFormSet):
    def get_form_kwargs(self, index):
        kwargs = super(AddFormIndexIntoKwargsFormSet, self).get_form_kwargs(index)
        kwargs['form_index'] = index
        return kwargs
    

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
        fields = ['id', 'status', 'entry', 'section']
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

