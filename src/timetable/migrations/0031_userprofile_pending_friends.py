# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0030_auto_20151013_1219'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='pending_friends',
            field=models.ManyToManyField(related_name='pendingFriends', to='timetable.UserProfile', blank=True),
        ),
    ]
