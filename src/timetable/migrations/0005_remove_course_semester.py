# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0004_auto_20150920_1240'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='semester',
        ),
    ]
