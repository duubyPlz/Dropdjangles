# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0020_user_timetable'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='timetable',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
