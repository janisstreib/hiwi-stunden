# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hiwi_portal', '0018_auto_20160103_2026'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='worklog',
            name='overWork',
        ),
    ]
