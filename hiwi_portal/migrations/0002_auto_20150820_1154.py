# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hiwi_portal', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Carer',
            new_name='Supervisor',
        ),
        migrations.RenameField(
            model_name='contract',
            old_name='carer',
            new_name='supervisor',
        ),
        migrations.AlterField(
            model_name='user',
            name='kitaccount',
            field=models.CharField(max_length=32),
        ),
    ]
