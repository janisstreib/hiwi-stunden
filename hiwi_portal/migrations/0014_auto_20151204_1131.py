# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('hiwi_portal', '0013_auto_20151201_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='hours',
            field=models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(85)]),
        ),
    ]
