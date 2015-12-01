# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hiwi_portal', '0011_contract_vacation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worktime',
            name='pause',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
