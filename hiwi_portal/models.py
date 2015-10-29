# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import UserManager

#
class User(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    kitaccount = models.CharField(max_length=32, unique=True) #funfact: old MS legacy :)
    email = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField()
    REQUIRED_FIELDS = ['firstname', 'lastname', 'email']
    USERNAME_FIELD = 'kitaccount'
    objects = UserManager()

    def set_unusable_password():
        pass;
    def get_username(self):
        return self.kitaccount
    def is_authenticated(self):
        return True
    def set_password(self, pw):
        pass;
class Hiwi(User):
    pass

class Department(models.Model):
    name = models.CharField(max_length=200)

class Supervisor(User):
    department = models.ForeignKey(Department)

class Contract(models.Model):
    PERSONELL_DEPARTMENTS = (
        ('GF', 'Großforschungsbereich'),
        ('UF', 'Universitätsbereich'),
    )
    user =  models.ForeignKey(Hiwi)
    supervisor = models.ForeignKey(Supervisor)
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
