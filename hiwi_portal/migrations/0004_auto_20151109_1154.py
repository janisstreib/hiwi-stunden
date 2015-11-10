# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('hiwi_portal', '0003_auto_20151030_1829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='department',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='user',
            name='private_email',
            field=models.CharField(blank=True, max_length=200, null=True, validators=[django.core.validators.EmailValidator()]),
        ),
    ]
