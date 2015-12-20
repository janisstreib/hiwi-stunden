# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hiwi_portal', '0015_worklog_overwork'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='work_dusted',
            field=models.BooleanField(default=False),
        ),
    ]
