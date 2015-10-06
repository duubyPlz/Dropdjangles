# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0003_auto_20150917_0611'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='day',
            field=models.IntegerField(default=0, choices=[(0, b'Monday'), (1, b'Tuesday'), (2, b'Wednesday'), (3, b'Thursday'), (4, b'Friday'), (5, b'Saturday'), (6, b'Sunday')]),
        ),
        migrations.AddField(
            model_name='course',
            name='semester',
            field=models.IntegerField(default=0, choices=[(0, b'One'), (1, b'Two')]),
        ),
        migrations.AddField(
            model_name='course',
            name='year',
            field=models.IntegerField(default=2015),
        ),
    ]
