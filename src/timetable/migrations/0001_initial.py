# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import swampdragon.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'Not specified', max_length=20)),
                ('time_from', models.CharField(default=b'0', max_length=10)),
                ('time_to', models.CharField(default=b'0', max_length=10)),
                ('day', models.IntegerField(default=0, choices=[(0, b'Monday'), (1, b'Tuesday'), (2, b'Wednesday'), (3, b'Thursday'), (4, b'Friday'), (5, b'Saturday'), (6, b'Sunday')])),
                ('classtype', models.CharField(default=b'Not specified', max_length=70)),
                ('enrols', models.IntegerField(default=0)),
                ('capacity', models.IntegerField(default=0)),
                ('room', models.CharField(default=b'Not specified', max_length=170)),
            ],
            bases=(swampdragon.models.SelfPublishModel, models.Model),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('year', models.IntegerField(default=2015)),
                ('semester', models.IntegerField(default=0, choices=[(0, b'One'), (1, b'Two')])),
            ],
            bases=(swampdragon.models.SelfPublishModel, models.Model),
        ),
        migrations.CreateModel(
            name='Timetable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'15s2', max_length=100)),
                ('classes', models.ManyToManyField(related_name='timetable', to='timetable.Class', blank=True)),
                ('courses', models.ManyToManyField(to='timetable.Course', blank=True)),
            ],
            bases=(swampdragon.models.SelfPublishModel, models.Model),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('friends', models.ManyToManyField(to='timetable.UserProfile', blank=True)),
                ('pending_friends', models.ManyToManyField(related_name='pendingFriends', to='timetable.UserProfile', blank=True)),
                ('timetable', models.OneToOneField(null=True, blank=True, to='timetable.Timetable')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(to='timetable.Timetable'),
        ),
        migrations.AddField(
            model_name='class',
            name='course',
            field=models.ForeignKey(to='timetable.Course', null=True),
        ),
        migrations.AddField(
            model_name='class',
            name='shared_stream',
            field=models.ManyToManyField(related_name='shared_stream_classes', to='timetable.Class', blank=True),
        ),
    ]
