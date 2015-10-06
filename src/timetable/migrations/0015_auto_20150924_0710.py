# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0014_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='classtype',
            field=models.IntegerField(choices=[(0, 'Lecture'), (1, 'Tutorial'), (2, 'Lab')], default=0),
        ),
        migrations.AlterField(
            model_name='class',
            name='day',
            field=models.IntegerField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')], default=0),
        ),
        migrations.AlterField(
            model_name='course',
            name='semester',
            field=models.IntegerField(choices=[(0, 'One'), (1, 'Two')], default=0),
        ),
    ]
