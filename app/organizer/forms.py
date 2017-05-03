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
                


"""
SL Edit Order/Lane
"""
class SLEditForm(forms.ModelForm):
    bib = forms.CharField(widget=forms.HiddenInput())
    name = forms.CharField(widget=forms.HiddenInput())
    kana = forms.CharField(widget=forms.HiddenInput())
    grade = forms.CharField(widget=forms.HiddenInput())
    club = forms.CharField(widget=forms.HiddenInput())
    pb = forms.CharField(widget=forms.HiddenInput())
    status = forms.CharField(widget=forms.HiddenInput())

    
    class Meta:
        model = Entry
        fields = ['id', 'group', 'order_lane']
        widgets = {
            'group': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'placeholder':'組'}),
            'order_lane': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'placeholder':'レーン/試技順'})
        }

        
    def __init__(self, *args, **kwargs):
        entry = kwargs['instance']
        super(SLEditForm, self).__init__(*args, **kwargs)
        self.fields["bib"].initial = entry.bib
        self.fields["name"].initial =  entry.name_family+" "+entry.name_first
        self.fields["kana"].initial =  entry.kana_family+" "+entry.kana_first
        self.fields["grade"].initial = entry.grade
        self.fields["club"].initial =  entry.club
        self.fields["pb"].initial =  entry.personal_best
        self.fields["status"].initial =  entry.entry_status

        self.fields["group"].widget.attrs.update()
        self.fields["order_lane"].widget.attrs.update({'class': 'form-control form-control-sm', 'placeholder':'レーン/試技順'})

