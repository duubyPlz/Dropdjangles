# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0019_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='timetable',
            field=models.OneToOneField(null=True, blank=True, to='timetable.Timetable'),
        ),
    ]
