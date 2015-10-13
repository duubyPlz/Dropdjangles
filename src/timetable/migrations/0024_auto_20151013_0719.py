# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0023_auto_20151013_0711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='timetable',
            field=models.ForeignKey(null=True, blank=True, to='timetable.Timetable', unique=True),
        ),
    ]
