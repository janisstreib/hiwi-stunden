# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hiwi_portal', '0006_auto_20151110_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worklog',
            name='carer_signed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='worklog',
            name='printed',
            field=models.BooleanField(default=False),
        ),
    ]
