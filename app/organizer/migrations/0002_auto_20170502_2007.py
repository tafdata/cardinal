# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-02 11:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competitions', '0001_initial'),
        ('organizer', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='entry',
            unique_together=set([('bib', 'event_status', 'group', 'order_lane')]),
        ),
    ]
