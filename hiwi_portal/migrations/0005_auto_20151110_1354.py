# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hiwi_portal', '0004_auto_20151109_1154'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contract',
            name='supervisor',
        ),
        migrations.AlterField(
            model_name='contract',
            name='personell',
            field=models.CharField(max_length=2, choices=[(b'GF', b'Gro\xc3\x9fforschungsbereich'), (b'UB', b'Universit\xc3\xa4tsbereich')]),
        ),
    ]
