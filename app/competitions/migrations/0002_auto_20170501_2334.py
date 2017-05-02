# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-01 14:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competitions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventstatus',
            name='section',
            field=models.CharField(choices=[('VS', '対校'), ('OP', 'OP'), ('TT', '記録会'), ('XX', 'その他')], default='OP', max_length=2),
        ),
    ]
