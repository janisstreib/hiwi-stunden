# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hiwi_portal', '0007_auto_20151110_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='worktime',
            name='activity',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
