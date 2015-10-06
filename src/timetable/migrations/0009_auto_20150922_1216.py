# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0008_classinstance_courseinstance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='class',
            name='timetable',
        ),
        migrations.AddField(
            model_name='class',
            name='course',
            field=models.ForeignKey(to='timetable.Course', null=True),
        ),
    ]
