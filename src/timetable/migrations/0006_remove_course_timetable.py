# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0005_remove_course_semester'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='timetable',
        ),
    ]
