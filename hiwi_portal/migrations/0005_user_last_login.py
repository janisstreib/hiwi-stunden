# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('hiwi_portal', '0004_user_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_login',
            field=models.DateField(default=datetime.datetime(2015, 10, 29, 16, 9, 36, 454631, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
