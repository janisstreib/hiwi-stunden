# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hours', models.IntegerField()),
                ('payment', models.DecimalField(max_digits=6, decimal_places=2)),
                ('personell', models.CharField(max_length=2, choices=[(b'GF', b'Gro\xc3\x9fforschungsbereich'), (b'UF', b'Universit\xc3\xa4tsbereich')])),
                ('personell_number', models.IntegerField()),
                ('contract_begin', models.DateField(verbose_name=b'Vertragsstart')),
                ('contract_end', models.DateField(verbose_name=b'Vertragsende')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('firstname', models.CharField(max_length=200)),
                ('lastname', models.CharField(max_length=200)),
                ('kitaccount', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='WorkLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('printed', models.BooleanField()),
                ('carer_signed', models.BooleanField()),
                ('contract', models.ForeignKey(to='hiwi_portal.Contract')),
            ],
        ),
        migrations.CreateModel(
            name='WorkTime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hours', models.IntegerField()),
                ('pause', models.IntegerField()),
                ('begin', models.DateTimeField(verbose_name=b'Start')),
                ('end', models.DateTimeField(verbose_name=b'Ende')),
                ('work_log', models.ForeignKey(to='hiwi_portal.WorkLog')),
            ],
        ),
        migrations.CreateModel(
            name='Carer',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='hiwi_portal.User')),
                ('department', models.ForeignKey(to='hiwi_portal.Department')),
            ],
            bases=('hiwi_portal.user',),
        ),
        migrations.CreateModel(
            name='Hiwi',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='hiwi_portal.User')),
            ],
            bases=('hiwi_portal.user',),
        ),
        migrations.AddField(
            model_name='contract',
            name='department',
            field=models.ForeignKey(to='hiwi_portal.Department'),
        ),
        migrations.AddField(
            model_name='contract',
            name='carer',
            field=models.ForeignKey(to='hiwi_portal.Carer'),
        ),
        migrations.AddField(
            model_name='contract',
            name='user',
            field=models.ForeignKey(to='hiwi_portal.Hiwi'),
        ),
    ]
