# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hiwi_portal', '0012_auto_20151201_1035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='personell_number',
            field=models.CharField(max_length=200),
        ),
    ]
