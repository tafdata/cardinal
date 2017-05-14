from django.db import models
from competitions.models import Comp, Event, EventStatus
from competitions.models import COMP_STATUS_CHOICES, SEX_CHOICES


# Create your models here.
ENTRY_STATUS_CHOICES = (
    ('Entry', 'Entry'),
    ('Entry_2', 'Entry_2'),     # 当日エントリーなど
    ('stand_by', 'StandBy'),
    ('Finish', 'Finish'),
    ('DNS', 'DNS'),
    ('DNF', 'DNF'),
    ('DQ', 'DQ'),
    ('NM', 'NM'),
    ('NH', 'NH'),
)
    
"""
Entry: エントリー
"""
class Entry(models.Model):
    id = models.AutoField(primary_key=True)
    event_status = models.ForeignKey('competitions.EventStatus')
    bib = models.CharField(max_length=64, blank=True)
    name_family = models.CharField("family name", max_length=64, help_text="姓")
    name_first = models.CharField("first name", max_length=64, help_text="名")
    kana_family = models.CharField(max_length=64, help_text="セイ")
    kana_first = models.CharField(max_length=64, help_text="メイ")
    sex = models.CharField(
        max_length=4,
        choices=SEX_CHOICES,
        default='U',
    )
    grade = models.CharField(max_length=64, blank=True, help_text="ex. B4")
    club  = models.CharField(max_length=256, blank=True, help_text="ex. 大阪大")
    jaaf_branch = models.CharField(max_length=64) # 登録陸協
    personal_best = models.CharField(max_length=6, blank=True)
    group = models.IntegerField(default=-1)      # 組
    order_lane = models.IntegerField(default=-1) # レーン/試技順
    entry_status = models.CharField(
        max_length=64,
        choices=ENTRY_STATUS_CHOICES,
        default='Entry'
    )
    check = models.BooleanField(default=False)  # スタートリスト出力時に赤文字

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return str(self.event_status)+"["+str(self.name_family)+str(self.name_first)+"]"

    
    class Meta:
        unique_together = (('event_status', 'bib'),)

