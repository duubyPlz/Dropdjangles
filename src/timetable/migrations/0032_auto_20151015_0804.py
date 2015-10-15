# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0031_userprofile_pending_friends'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='class',
            name='students',
        ),
        migrations.AlterField(
            model_name='timetable',
            name='classes',
            field=models.ManyToManyField(related_name='timetable', to='timetable.Class', blank=True),
        ),
    ]
