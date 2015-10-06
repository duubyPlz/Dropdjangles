# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import swampdragon.models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0007_course_semester'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('base', models.ForeignKey(to='timetable.Class')),
                ('user', models.ForeignKey(to='timetable.Timetable')),
            ],
            bases=(swampdragon.models.SelfPublishModel, models.Model),
        ),
        migrations.CreateModel(
            name='CourseInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('base', models.ForeignKey(to='timetable.Course')),
                ('user', models.ForeignKey(to='timetable.Timetable')),
            ],
            bases=(swampdragon.models.SelfPublishModel, models.Model),
        ),
    ]
