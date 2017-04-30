from django.db import models

# Create your models here.
"""
Choice Options
"""
STATUS_CHOICES = (
    ('lock', 'Lock'),
    ('entry', 'Entry'),
    ('standby', 'Stand By'),
    ('result', 'Result'),
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
        choices=STATUS_CHOICES,
        default='lock',
    )   # entry/result/on_going
    
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


"""
Event: 種目
"""
class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    short = models.CharField(max_length=256)
    sex = models.CharField(max_length=4)      # M/W
    order = models.CharField(max_length=4)
    separator_1 = models.CharField(max_length=4, blank=True)
    separator_2 = models.CharField(max_length=4, blank=True)
    separator_3 = models.CharField(max_length=4, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name+"["+self.sex+"]"
    

"""
EventStatus: 種目の実施状況
"""
class EventStatus(models.Model):
    id = models.AutoField(primary_key=True)
    comp = models.ForeignKey('Comp')
    event = models.ForeignKey('Event')
    status = models.CharField(
        max_length=16,
        choices=STATUS_CHOICES,
        default='lock',
    )   # entry/result/on_going
    entry = models.BooleanField(default=False) # エントリーの可否
    section = models.CharField(max_length=64) # 対校/OP

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.event)+"["+str(self.comp)+"]"


    
    
    
    


