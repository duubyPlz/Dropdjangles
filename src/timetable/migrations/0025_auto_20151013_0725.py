# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('timetable', '0024_auto_20151013_0719'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='timetable',
        ),
        migrations.AddField(
            model_name='timetable',
            name='owner',
            field=models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]
