# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models
import django.core.validators
from django.conf import settings


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
                ('kitaccount', models.CharField(unique=True, max_length=32)),
                ('email', models.CharField(max_length=200)),
                ('private_email', models.CharField(max_length=200, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('last_login', models.DateTimeField()),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])),
            ],
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
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
            name='Hiwi',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='hiwi_portal.User')),
            ],
            bases=('hiwi_portal.user',),
        ),
        migrations.CreateModel(
            name='Supervisor',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='hiwi_portal.User')),
                ('department', models.ForeignKey(to='hiwi_portal.Department')),
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
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contract',
            name='supervisor',
            field=models.ForeignKey(to='hiwi_portal.Supervisor'),
        ),
    ]
