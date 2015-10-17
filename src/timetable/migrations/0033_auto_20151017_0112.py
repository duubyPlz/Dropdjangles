# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0032_auto_20151015_0804'),
    ]

    operations = [
        migrations.RenameField(
            model_name='class',
            old_name='timeFrom',
            new_name='time_from',
        ),
        migrations.RenameField(
            model_name='class',
            old_name='timeTo',
            new_name='time_to',
        ),
        migrations.AddField(
            model_name='class',
            name='shared_stream',
            field=models.ManyToManyField(related_name='shared_stream_classes', to='timetable.Class', blank=True),
        ),
    ]
