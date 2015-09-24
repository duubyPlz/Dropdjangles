# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0012_auto_20150923_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='students',
            field=models.ManyToManyField(to='timetable.Timetable', blank=True),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='classes',
            field=models.ManyToManyField(to='timetable.Class', blank=True),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='courses',
            field=models.ManyToManyField(to='timetable.Course', blank=True),
        ),
    ]
