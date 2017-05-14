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
        fields = ['event_status', 'bib', 'name_family', 'name_first', 'kana_family', 'kana_first', 'sex', 'grade', 'club', 'jaaf_branch', 'personal_best', 'entry_status']

    def __init__(self, *args, **kwargs):
        try:
            event_status = kwargs.pop('event_status')
        except KeyError:
            event_status = False
        try:
            entry = kwargs['instance']
        except KeyError:
            entry = False
        super(EntryForm, self).__init__(*args, **kwargs)
        self.fields["event_status"].widget.attrs.update({'class': 'form-control form-control-sm'})
        if event_status:
            self.fields["event_status"].widget = forms.HiddenInput()
            self.fields["event_status"].initial = event_status.id

        self.fields["bib"].widget.attrs.update({'class': 'form-control form-control-sm'})
        self.fields["name_family"].widget.attrs.update({'class': 'form-control form-control-sm', 'placeholder':'姓'})
        self.fields["name_first"].widget.attrs.update({'class': 'form-control form-control-sm', 'placeholder':'名'})
        self.fields["kana_family"].widget.attrs.update({'class': 'form-control form-control-sm', 'placeholder':'セイ'})
        self.fields["kana_first"].widget.attrs.update({'class': 'form-control form-control-sm', 'placeholder':'メイ'})
        self.fields["kana_first"].required = False
        self.fields["sex"].widget.attrs.update({'class': 'form-control form-control-sm'})
        self.fields["grade"].widget.attrs.update({'class': 'form-control form-control-sm'})
        self.fields["club"].widget.attrs.update({'class': 'form-control form-control-sm'})
        self.fields["jaaf_branch"].widget.attrs.update({'class': 'form-control form-control-sm'})
        self.fields["personal_best"].widget.attrs.update({'class': 'form-control form-control-sm', 'placeholder':'ex. 001234'})
        if entry:
            self.fields["entry_status"].widget.attrs.update({'class': 'form-control form-control-sm'})
        else:
            self.fields["entry_status"].widget = forms.HiddenInput()
            self.fields["entry_status"].initial = 'None'

        
"""
Entry Add [一括]
"""
ENTRY_STATUS_CHOICES = (
    ('Entry', '通常エントリー'),
    ('Entry_2', '当日エントリーetc'),
)

class EntryUploadFileForm(forms.Form):
    file = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control-file', 'accept': 'text/csv'})
    )
    entry_status = forms.ChoiceField(
        choices=ENTRY_STATUS_CHOICES,
        initial='Entry',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    



        

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

    
    class Meta:
        model = Entry
        fields = ['id', 'group', 'order_lane', 'entry_status']
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

        self.fields["group"].widget.attrs.update()
        self.fields["order_lane"].widget.attrs.update({'class': 'form-control form-control-sm', 'placeholder':'レーン/試技順'})
        self.fields["entry_status"].widget.attrs.update({'class': 'form-control form-control-sm', 'placeholder':'レーン/試技順'})




"""
Entry Edit Entry Status
"""
class EntryStatusEditForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['id','entry_status']

        
    def __init__(self, *args, **kwargs):
        try:
            mode = kwargs.pop('mode')
        except KeyError:
            mode = False
        super(EntryStatusEditForm, self).__init__(*args, **kwargs)
        if mode == 'simple':
            self.fields["entry_status"].widget = forms.HiddenInput()



"""
Entry Edit Entry Status
"""
class SLUpdateForm(forms.ModelForm):
    # comp = forms.CharField(widget=forms.HiddenInput())
    # event = forms.CharField(widget=forms.HiddenInput())
    # sex = forms.CharField(widget=forms.HiddenInput())
    # match_round = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = EventStatus
        fields = ['status', 'start_list', 'start_list_2']
        
    def __init__(self, *args, **kwargs):
        # event_status = kwargs.["instance"]
        super(SLUpdateForm, self).__init__(*args, **kwargs)
        self.fields["status"].widget.attrs.update({'class': 'form-control form-control-sm'})
        self.fields["start_list"].widget.attrs.update({'class': 'form-control form-control-sm'})
        self.fields["start_list_2"].widget.attrs.update({'class': 'form-control form-control-sm'})


"""
DNS Form
"""
class DNSForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['entry_status']
        widgets = {
            'id' : forms.HiddenInput(),
            'entry_status' : forms.HiddenInput(),
        }
