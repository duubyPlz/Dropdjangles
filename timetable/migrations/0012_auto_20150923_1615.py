# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0011_auto_20150923_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='students',
            field=models.ManyToManyField(to='timetable.Timetable', null=True),
        ),
    ]
