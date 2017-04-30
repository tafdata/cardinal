from django.db import models
from competitions.models import Event


# Create your models here.
"""
Entry: エントリー
"""
class Entry(models.Model):
    id = models.AutoField(primary_key=True)
    bib = models.CharField(max_length=64, blank=True)
    name_family = models.CharField(max_length=64)
    name_first = models.CharField(max_length=64)
    kana_family = models.CharField(max_length=64)
    kana_first = models.CharField(max_length=64)        
    grade = models.CharField(max_length=64, blank=True)
    club  = models.CharField(max_length=256, default='None')
    jaaf_branch = models.CharField(max_length=64) # 登録陸協
    personal_best = models.CharField(max_length=6, blank=True)
    event = models.ForeignKey('competitions.Event')
    group = models.CharField(max_length=64, blank=True)
    position = models.CharField(max_length=64, blank=True)
    sex = models.CharField(max_length=4)
    status = models.CharField(max_length=64, blank=True)
    
    def __str__(self):
        return str(id)
