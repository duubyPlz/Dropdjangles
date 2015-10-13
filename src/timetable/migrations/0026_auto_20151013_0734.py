# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0025_auto_20151013_0725'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timetable',
            name='owner',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='timetable',
            field=models.OneToOneField(null=True, blank=True, to='timetable.Timetable'),
        ),
    ]
