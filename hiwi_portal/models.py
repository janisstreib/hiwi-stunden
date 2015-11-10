# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import UserManager
from django.core.validators import RegexValidator
from django.core.validators import EmailValidator
#
class User(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    kitaccount = models.CharField(max_length=32, unique=True) #funfact: old MS legacy :)
    email = models.CharField(max_length=200)
    private_email = models.CharField(max_length=200, null=True, validators=[EmailValidator()], blank=True)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True, null=True)
    REQUIRED_FIELDS = ['firstname', 'lastname', 'email']
    USERNAME_FIELD = 'kitaccount'
    objects = UserManager()
    notify_to_private = models.BooleanField(default=False)

    def set_unusable_password(self):
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
        ('UB', 'Universitätsbereich'),
    )
    user =  models.ForeignKey(Hiwi)
    department = models.CharField(max_length=200)
    hours = models.IntegerField()
    payment = models.DecimalField(max_digits=6, decimal_places=2)
    personell = models.CharField(max_length=2, choices=PERSONELL_DEPARTMENTS)
    personell_number = models.IntegerField()
    contract_begin = models.DateField('Vertragsstart')
    contract_end = models.DateField('Vertragsende')

    @property
    def current_worklog(self):
        return self.cw

class WorkLog(models.Model):
    contract = models.ForeignKey(Contract)
    printed = models.BooleanField(default=False)
    carer_signed = models.BooleanField(default=False)
    month = models.IntegerField()
    year = models.IntegerField()

class WorkTime(models.Model):
    work_log =  models.ForeignKey(WorkLog)
    hours = models.IntegerField()
    pause = models.IntegerField()
    begin = models.TimeField('Start')
    end = models.TimeField('Ende')
    date = models.DateField()
    activity = models.CharField(max_length=200)
