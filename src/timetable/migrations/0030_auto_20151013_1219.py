# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0029_remove_userprofile_full_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='friends',
            field=models.ManyToManyField(to='timetable.UserProfile', blank=True),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='name',
            field=models.CharField(default=b'15s2', max_length=100),
        ),
    ]
