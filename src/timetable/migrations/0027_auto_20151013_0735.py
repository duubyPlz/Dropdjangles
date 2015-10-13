# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0026_auto_20151013_0734'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='timetable',
        ),
        migrations.AddField(
            model_name='timetable',
            name='owner',
            field=models.OneToOneField(null=True, blank=True, to='timetable.UserProfile'),
        ),
    ]
