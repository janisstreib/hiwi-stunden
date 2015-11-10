# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hiwi_portal', '0005_auto_20151110_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='worklog',
            name='month',
            field=models.IntegerField(default=-1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='worklog',
            name='year',
            field=models.IntegerField(default=-1),
            preserve_default=False,
        ),
    ]
