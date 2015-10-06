# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0015_auto_20150924_0710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='timeFrom',
            field=models.IntegerField(default=2, choices=[(0, b'8am'), (1, b'8:30am'), (2, b'9am'), (3, b'9:30am'), (4, b'10am'), (5, b'10:30am')]),
        ),
    ]
