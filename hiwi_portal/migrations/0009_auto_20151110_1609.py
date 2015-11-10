# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('hiwi_portal', '0008_worktime_activity'),
    ]

    operations = [
        migrations.AddField(
            model_name='worktime',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 11, 10, 16, 9, 45, 573599, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='worktime',
            name='begin',
            field=models.TimeField(verbose_name=b'Start'),
        ),
        migrations.AlterField(
            model_name='worktime',
            name='end',
            field=models.TimeField(verbose_name=b'Ende'),
        ),
    ]
