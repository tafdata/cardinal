# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-05 08:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizer', '0004_auto_20170505_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='group',
            field=models.IntegerField(blank=True, default=None),
        ),
        migrations.AlterField(
            model_name='entry',
            name='order_lane',
            field=models.IntegerField(blank=True, default=None),
        ),
    ]
