# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('hiwi_portal', '0002_auto_20151030_1355'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='notify_to_private',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='private_email',
            field=models.CharField(max_length=200, null=True, validators=[django.core.validators.EmailValidator()]),
        ),
    ]
