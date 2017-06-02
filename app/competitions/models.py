from django.db import models


# Create your models here.
"""
Choice Options
"""
COMP_STATUS_CHOICES = (
    ('Entry', 'Entry'),
    ('StandBy', 'Stand By'),
    ('OnGoing', 'On Going'),
    ('Result', 'Result'),
)

SEX_CHOICES = (
    ('M', '男'),
    ('W', '女'),
    ('U', 'Unknown'),
)

ORDER_CHOICES = (
    ('ASC', 'ASC'),
    ('DESC', 'DESC'),
)

SECTION_CHOICES = (
    ('VS', '対校'),
    ('OP', 'OP'),
    ('TT', '記録会'),
    ('XX', 'その他'),
)
CLASS_CHOICES = SECTION_CHOICES


ROUND_CHOICES = (
    ('Heats', 'Heats'),
    ('Qualification', 'Qualification'),
    ('Semifinal', 'Semifinal'),
    ('Final', 'Final'),
)
PROGRAM_TYPE_CHOICES = (
    ('Track8', 'トラック(セパレートスタート)'),
    ('TrackN', 'トラック(オープンレーンスタート)'),
    ('HJPV', '走高跳,棒高跳'),
    ('LJTJ', '走幅跳,三段跳'),
    ('Throw', '投擲競技'),
)
    



####################################
## Models
####################################

"""
Comp: 大会
"""
class Comp(models.Model):
    code = models.CharField(max_length=16, primary_key=True)
    name = models.CharField(max_length=512)
    place = models.CharField(max_length=256)
    place_code = models.CharField(max_length=16)
    date = models.DateField()
    sponsor = models.CharField(max_length=512, blank=True)
    organizer = models.CharField(max_length=512, blank=True)
    status = models.CharField(
        max_length=16,
        choices=COMP_STATUS_CHOICES,
        default='lock',
    )   # entry/result/on_going
    cardinal_organizer = models.BooleanField('競技会運営ツール使用', default=False) # Organizerを使用して運営==>True
    
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


"""
Event: 競技種目
"""
class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    short = models.CharField(max_length=256, blank=True)
    sex = models.CharField(
        max_length=1,
        choices=SEX_CHOICES,
        default='U',
    )      # M/W
    order = models.CharField(
        max_length=4,
        choices=ORDER_CHOICES,
        default='ASC',
    )
    program_type =  models.CharField(
        max_length=8,
        choices=PROGRAM_TYPE_CHOICES,
        default='Track8',
    )
    wind = models.BooleanField(default=True)
    separator_1 = models.CharField(max_length=4, blank=True)
    separator_2 = models.CharField(max_length=4, blank=True)
    separator_3 = models.CharField(max_length=4, blank=True)
    start_list_priority = models.IntegerField(default=999999)      # プログラム記載順

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.sex)+self.name

    
    class Meta:
        unique_together = ('name', 'sex')    


        
"""
EventStatus: 種目の実施状況
"""
class EventStatus(models.Model):
    id = models.AutoField(primary_key=True)
    comp = models.ForeignKey('Comp')
    event = models.ForeignKey('Event')
    status = models.CharField(
        max_length=16,
        choices=COMP_STATUS_CHOICES,
        default='lock',
    )   # entry/result/on_going
    section = models.CharField(
        max_length=4,
        choices=SECTION_CHOICES,
        default='OP',        
    ) # 対校/OP
    match_round = models.CharField(
        "Round",
        max_length=64,
        choices=ROUND_CHOICES,
        default='Final',
    )
    start_list_priority = models.IntegerField(default=999999)      # プログラム記載順
    start_list = models.BooleanField(default=False)  # スタートリストを出力
    start_list_2 = models.BooleanField(default=False)  # スタートリスト(最終版)を出力

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "comp"+str(self.comp.code)+"_"+str(self.section)+"_"+str(self.event)


    class Meta:
        unique_together = ('comp', 'event', 'section', 'match_round')


    
    
    

"""
GR 大会記録
"""
class GR(models.Model):
    id = models.AutoField(primary_key=True)
    comp = models.ForeignKey('Comp')
    event = models.ForeignKey('Event')
    mark = models.CharField(max_length=6, blank=True)
    name_family = models.CharField("family name", max_length=64, help_text="姓")
    name_first = models.CharField("first name", max_length=64, help_text="名")
    club  = models.CharField(max_length=256, blank=True, help_text="ex. 大阪大")
    year = models.IntegerField(default=-1) # レーン/試技順

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return "GR_"+str(self.comp)+str(self.event)
    
    class Meta:
        unique_together = ('comp', 'event')



"""
Result 記録
"""
from organizer.models import Entry
class Result(models.Model):
    id = models.AutoField(primary_key=True)
    comp = models.ForeignKey('Comp',on_delete=models.PROTECT)
    event = models.ForeignKey('Event',on_delete=models.PROTECT)
    sex = models.CharField(
        max_length=1,
        choices=SEX_CHOICES,
        default='U',
    )      # M/W
    game_class = models.CharField(
        max_length=4,
        choices=CLASS_CHOICES,
        default='OP',        
    ) # 部門 [対校/OP]
    game_round = models.CharField(
        "Round",
        max_length=64,
        choices=ROUND_CHOICES,
        default='Final',
    )
    group = models.IntegerField()      # 組
    position = models.IntegerField(blank=True) # 順位
    order_lane = models.IntegerField() # レーン/試技順
    bib = models.CharField(max_length=64, blank=True)
    name = models.CharField(max_length=64, help_text="氏名")
    kana = models.CharField(max_length=64, help_text="フリガナ")
    grade = models.CharField(max_length=64, blank=True)
    club  = models.CharField(max_length=256, blank=True)
    jaaf_branch = models.CharField(max_length=64) # 登録陸協
    mark = models.CharField(max_length=6, blank=True)
    wind = models.FloatField(blank=True, null=True)
    
    entry = models.ForeignKey(
        'organizer.Entry',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )                           # 記録プロの出力には必要


    def __str__(self):
        return str(self.comp)+str(self.event)+str(self.name)
    
    
    class Meta:
        unique_together = ('comp', 'event', 'game_class', 'game_round', 'bib')
