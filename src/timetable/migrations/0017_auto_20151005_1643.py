# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0016_auto_20150924_0746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='timeFrom',
            field=models.IntegerField(default=2, choices=[(0, b'8:00'), (1, b'8:30'), (2, b'9:00'), (3, b'9:30'), (4, b'10:00'), (5, b'10:30'), (6, b'11:00'), (7, b'11:30'), (8, b'12:00'), (9, b'12:30'), (10, b'13:00'), (11, b'13:30'), (12, b'14:00'), (13, b'14:30'), (14, b'15:00'), (15, b'15:30'), (16, b'16:00'), (17, b'16:30'), (18, b'17:00'), (19, b'17:30'), (20, b'18:00'), (21, b'18:30'), (22, b'19:00'), (23, b'19:30'), (24, b'20:00'), (25, b'20:30'), (26, b'21:00'), (27, b'21:30')]),
        ),
        migrations.AlterField(
            model_name='class',
            name='timeTo',
            field=models.IntegerField(default=4, choices=[(0, b'8:00'), (1, b'8:30'), (2, b'9:00'), (3, b'9:30'), (4, b'10:00'), (5, b'10:30'), (6, b'11:00'), (7, b'11:30'), (8, b'12:00'), (9, b'12:30'), (10, b'13:00'), (11, b'13:30'), (12, b'14:00'), (13, b'14:30'), (14, b'15:00'), (15, b'15:30'), (16, b'16:00'), (17, b'16:30'), (18, b'17:00'), (19, b'17:30'), (20, b'18:00'), (21, b'18:30'), (22, b'19:00'), (23, b'19:30'), (24, b'20:00'), (25, b'20:30'), (26, b'21:00'), (27, b'21:30')]),
        ),
    ]
