# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0009_auto_20150922_1216'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classinstance',
            name='base',
        ),
        migrations.RemoveField(
            model_name='classinstance',
            name='user',
        ),
        migrations.RemoveField(
            model_name='courseinstance',
            name='base',
        ),
        migrations.RemoveField(
            model_name='courseinstance',
            name='user',
        ),
        migrations.AddField(
            model_name='class',
            name='students',
            field=models.ManyToManyField(to='timetable.Timetable'),
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(to='timetable.Timetable'),
        ),
        migrations.AddField(
            model_name='timetable',
            name='classes',
            field=models.ManyToManyField(to='timetable.Class'),
        ),
        migrations.AddField(
            model_name='timetable',
            name='courses',
            field=models.ManyToManyField(to='timetable.Course'),
        ),
        migrations.AlterField(
            model_name='class',
            name='name',
            field=models.CharField(max_length=20),
        ),
        migrations.DeleteModel(
            name='ClassInstance',
        ),
        migrations.DeleteModel(
            name='CourseInstance',
        ),
    ]
