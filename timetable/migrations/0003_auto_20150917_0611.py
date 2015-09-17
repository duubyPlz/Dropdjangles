# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import swampdragon.models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0002_remove_timetable_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('timetable', models.ForeignKey(to='timetable.Timetable')),
            ],
            bases=(swampdragon.models.SelfPublishModel, models.Model),
        ),
        migrations.AddField(
            model_name='class',
            name='classtype',
            field=models.IntegerField(default=0, choices=[(0, b'Lecture'), (1, b'Tutorial'), (2, b'Lab')]),
        ),
    ]
