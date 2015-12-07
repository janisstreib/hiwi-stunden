# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hiwi_portal', '0014_auto_20151204_1131'),
    ]

    operations = [
        migrations.AddField(
            model_name='worklog',
            name='overWork',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
