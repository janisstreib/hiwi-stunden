# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('hiwi_portal', '0017_fillerworkdustactivity_fixedworkdustactivity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='worktime',
            name='date',
        ),
        migrations.AlterField(
            model_name='fixedworkdustactivity',
            name='week_day',
            field=models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(4)]),
        ),
        migrations.AlterField(
            model_name='worktime',
            name='begin',
            field=models.DateTimeField(verbose_name=b'Start'),
        ),
        migrations.AlterField(
            model_name='worktime',
            name='end',
            field=models.DateTimeField(verbose_name=b'Ende'),
        ),
    ]
