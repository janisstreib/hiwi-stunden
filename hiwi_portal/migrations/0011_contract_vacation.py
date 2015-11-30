# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hiwi_portal', '0010_auto_20151130_1257'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='vacation',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
