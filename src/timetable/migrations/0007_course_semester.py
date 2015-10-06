# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0006_remove_course_timetable'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='semester',
            field=models.IntegerField(default=0, choices=[(0, b'One'), (1, b'Two')]),
        ),
    ]
