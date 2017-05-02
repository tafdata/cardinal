from django import forms
from competitions.models  import Comp, Event, EventStatus
from competitions.models  import SECTION_CHOICES, SEX_CHOICES

from organizer.models import Entry


#
# Form
#
"""
運営競技会　選択
"""
class SelectCompForm(forms.Form):
    comp_code = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        comp_code = kwargs.pop("comp_code")
        super(SelectCompForm, self).__init__(*args, **kwargs)
        self.fields["comp_code"].initial = comp_code


"""
エントリー確認 | 絞り込み
"""
class EntryFilterForm(forms.Form):
    section = forms.ChoiceField(
        choices=SECTION_CHOICES,
        required=False,)
    event = forms.ModelChoiceField(
        queryset=Event.objects.none(),
        required=False,
        empty_label=None,)
    
    def __init__(self, comp=None, *args, **kwargs):
        super(EntryFilterForm, self).__init__(*args, **kwargs)
        self.fields["section"].widget.attrs.update({'class': 'form-control form-control-sm'})
        self.fields["event"].queryset = self.get_event_list(comp)
        self.fields["event"].widget.attrs.update({'class': 'form-control form-control-sm'})

        
    def get_event_list(self, comp=None):
        event_ids = EventStatus.objects.filter(comp=comp).values_list('event', flat=True).order_by('event').distinct()
        events = Event.objects.filter(id__in=event_ids)
        print(event_ids)
        return events
            
        

"""
Entry Add [個別]
"""
class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['event_status', 'bib', 'name_family', 'name_first', 'kana_family', 'kana_first', 'sex', 'grade', 'club', 'jaaf_branch', 'personal_best' ]

    def __init__(self, *args, **kwargs):
        super(EntryForm, self).__init__(*args, **kwargs)
        self.fields["event_status"].widget.attrs.update({'class': 'form-control form-control-sm'})
        self.fields["bib"].widget.attrs.update({'class': 'form-control form-control-sm'})
        self.fields["name_family"].widget.attrs.update({'class': 'form-control form-control-sm', 'placeholder':'姓'})
        self.fields["name_first"].widget.attrs.update({'class': 'form-control form-control-sm', 'placeholder':'名'})
        self.fields["kana_family"].widget.attrs.update({'class': 'form-control form-control-sm', 'placeholder':'セイ'})
        self.fields["kana_first"].widget.attrs.update({'class': 'form-control form-control-sm', 'placeholder':'メイ'})
        self.fields["sex"].widget.attrs.update({'class': 'form-control form-control-sm'})
        self.fields["grade"].widget.attrs.update({'class': 'form-control form-control-sm', 'placeholder':'ex. B4'})
        self.fields["club"].widget.attrs.update({'class': 'form-control form-control-sm'})
        self.fields["jaaf_branch"].widget.attrs.update({'class': 'form-control form-control-sm'})
        self.fields["personal_best"].widget.attrs.update({'class': 'form-control form-control-sm', 'placeholder':'ex. 001234'})
                
