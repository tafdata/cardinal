# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-06-01 07:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competitions', '0011_auto_20170601_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='position',
            field=models.IntegerField(blank=True),
        ),
    ]
