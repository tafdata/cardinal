from django.db import models

# Create your models here.
"""
Choice Options
"""
COMP_STATUS_CHOICES = (
    ('Lock', 'Lock'),
    ('Entry', 'Entry'),
    ('StandBy', 'Stand By'),
    ('OnGoing', 'On Going'),
    ('Result', 'Result'),
)

SEX_CHOICES = (
    ('M', '男'),
    ('W', '女'),
    ('F', '家族'),
    ('X', 'その他'),
    ('U', 'Unknown'),
)

ORDER_CHOICES = (
    ('ASC', 'ASC'),
    ('DESC', 'DESC'),
)

SECTION_CHOICES = (
    ('VS', '対校'),
    ('OP', 'OP'),
    ('Sub', '補欠'),
    ('TT', '記録会'),
    ('XX', 'その他'),
)

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
    date_end = models.DateField(blank=True)
    sponsor = models.CharField(max_length=512, blank=True)
    organizer = models.CharField(max_length=512, blank=True)
    status = models.CharField(
        max_length=16,
        choices=COMP_STATUS_CHOICES,
        default='lock',
    )   # entry/result/on_going
    
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
    short = models.CharField(max_length=256)
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
    wind = models.BooleanField(default=False)
    separator_1 = models.CharField(max_length=4, blank=True)
    separator_2 = models.CharField(max_length=4, blank=True)
    separator_3 = models.CharField(max_length=4, blank=True)
    

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name+"["+str(self.sex)+"]"

    
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
    
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.section)+"_"+str(self.event)


    class Meta:
        unique_together = ('comp', 'event', 'section', 'match_round')


    
    
    
    


