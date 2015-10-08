# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0017_auto_20151005_1643'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='capacity',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='class',
            name='enrols',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='class',
            name='room',
            field=models.CharField(default=b'Not specified', max_length=170),
        ),
        migrations.AlterField(
            model_name='class',
            name='classtype',
            field=models.CharField(default=b'Not specified', max_length=70),
        ),
        migrations.AlterField(
            model_name='class',
            name='name',
            field=models.CharField(default=b'Not specified', max_length=20),
        ),
        migrations.AlterField(
            model_name='class',
            name='students',
            field=models.ManyToManyField(to='timetable.Timetable'),
        ),
        migrations.AlterField(
            model_name='class',
            name='timeFrom',
            field=models.CharField(default=b'0', max_length=10),
        ),
        migrations.AlterField(
            model_name='class',
            name='timeTo',
            field=models.CharField(default=b'0', max_length=10),
        ),
    ]
