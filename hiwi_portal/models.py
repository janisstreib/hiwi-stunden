# -*- coding: utf-8 -*-
from django.db import models

class User(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    kitaccount = models.CharField(max_length=200)

class Hiwi(User):
    pass

class Department(models.Model):
    name = models.CharField(max_length=200)

class Carer(User):
    department = models.ForeignKey(Department)

class Contract(models.Model):
    PERSONELL_DEPARTMENTS = (
        ('GF', 'Großforschungsbereich'),
        ('UF', 'Universitätsbereich'),
    )
    user =  models.ForeignKey(Hiwi)
    carer = models.ForeignKey(Carer)
    department = models.ForeignKey(Department)
    hours = models.IntegerField()
    payment = models.DecimalField(max_digits=6, decimal_places=2)
    personell = models.CharField(max_length=2, choices=PERSONELL_DEPARTMENTS)
    personell_number = models.IntegerField()
    contract_begin = models.DateField('Vertragsstart')
    contract_end = models.DateField('Vertragsende')

class WorkLog(models.Model):
    contract = models.ForeignKey(Contract)
    printed = models.BooleanField()
    carer_signed = models.BooleanField()

class WorkTime(models.Model):
    work_log =  models.ForeignKey(WorkLog)
    hours = models.IntegerField()
    pause = models.IntegerField()
    begin = models.DateTimeField('Start')
    end = models.DateTimeField('Ende')
