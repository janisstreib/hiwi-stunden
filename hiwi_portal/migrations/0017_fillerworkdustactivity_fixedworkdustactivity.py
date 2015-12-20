# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('hiwi_portal', '0016_user_work_dusted'),
    ]

    operations = [
        migrations.CreateModel(
            name='FIllerWorkDustActivity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=200)),
                ('avg_length', models.IntegerField()),
                ('contract', models.ForeignKey(to='hiwi_portal.Contract')),
            ],
        ),
        migrations.CreateModel(
            name='FixedWorkDustActivity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=200)),
                ('avg_length', models.IntegerField()),
                ('start', models.TimeField(verbose_name=b'Start')),
                ('week_day', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(6)])),
                ('contract', models.ForeignKey(to='hiwi_portal.Contract')),
            ],
        ),
    ]
