# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-02 09:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comp',
            fields=[
                ('code', models.CharField(max_length=16, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=512)),
                ('place', models.CharField(max_length=256)),
                ('place_code', models.CharField(max_length=16)),
                ('date', models.DateField()),
                ('date_end', models.DateField(blank=True)),
                ('sponsor', models.CharField(blank=True, max_length=512)),
                ('organizer', models.CharField(blank=True, max_length=512)),
                ('status', models.CharField(choices=[('Lock', 'Lock'), ('Entry', 'Entry'), ('StandBy', 'Stand By'), ('OnGoing', 'On Going'), ('Result', 'Result')], default='lock', max_length=16)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256)),
                ('short', models.CharField(max_length=256)),
                ('sex', models.CharField(choices=[('M', '男'), ('W', '女'), ('F', '家族'), ('X', 'その他'), ('U', 'Unknown')], default='U', max_length=1)),
                ('order', models.CharField(choices=[('ASC', 'ASC'), ('DESC', 'DESC')], default='ASC', max_length=4)),
                ('separator_1', models.CharField(blank=True, max_length=4)),
                ('separator_2', models.CharField(blank=True, max_length=4)),
                ('separator_3', models.CharField(blank=True, max_length=4)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='EventStatus',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('Lock', 'Lock'), ('Entry', 'Entry'), ('StandBy', 'Stand By'), ('OnGoing', 'On Going'), ('Result', 'Result')], default='lock', max_length=16)),
                ('section', models.CharField(choices=[('VS', '対校'), ('OP', 'OP'), ('TT', '記録会'), ('XX', 'その他')], default='OP', max_length=2)),
                ('match_round', models.CharField(choices=[('Heats', 'Heats'), ('Qualification', 'Qualification'), ('Semifinal', 'Semifinal'), ('Final', 'Final')], default='Final', max_length=64, verbose_name='Round')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('comp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='competitions.Comp')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='competitions.Event')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='event',
            unique_together=set([('name', 'sex')]),
        ),
        migrations.AlterUniqueTogether(
            name='eventstatus',
            unique_together=set([('comp', 'event', 'match_round')]),
        ),
    ]
