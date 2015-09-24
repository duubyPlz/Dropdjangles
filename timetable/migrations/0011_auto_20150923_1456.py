# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0010_auto_20150923_0607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timetable',
            name='classes',
            field=models.ManyToManyField(to='timetable.Class', null=True),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='courses',
            field=models.ManyToManyField(to='timetable.Course', null=True),
        ),
    ]
