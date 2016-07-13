# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import UserManager
from django.core.validators import RegexValidator
from django.core.validators import EmailValidator
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
import time
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError


#
class User(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    kitaccount = models.CharField(max_length=32, unique=True)  # funfact: old MS legacy :)
    email = models.CharField(max_length=200)
    private_email = models.CharField(max_length=200, null=True, validators=[EmailValidator()], blank=True)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True, null=True)
    REQUIRED_FIELDS = ['firstname', 'lastname', 'email']
    USERNAME_FIELD = 'kitaccount'
    objects = UserManager()
    notify_to_private = models.BooleanField(default=False)
    work_dusted = models.BooleanField(default=False)

    def set_unusable_password(self):
        pass

    def get_username(self):
        return self.kitaccount

    def is_authenticated(self):
        return True

    def set_password(self, pw):
        pass


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
    user = models.ForeignKey(Hiwi)
    department = models.CharField(max_length=200)
    hours = models.PositiveIntegerField(validators=[MaxValueValidator(85)])
    payment = models.DecimalField(max_digits=6, decimal_places=2)
    personell = models.CharField(max_length=2, choices=PERSONELL_DEPARTMENTS)
    personell_number = models.CharField(max_length=200)
    contract_begin = models.DateField('Vertragsstart')
    contract_end = models.DateField('Vertragsende')
    vacation = models.PositiveIntegerField()

    @property
    def current_worklog(self):
        return self.cw


class WorkLog(models.Model):
    contract = models.ForeignKey(Contract)
    printed = models.BooleanField(default=False)
    carer_signed = models.BooleanField(default=False)
    month = models.IntegerField()
    year = models.IntegerField()

    def getWorkLog(self, contract, month, year):
        try:
            if contract.contract_begin.year > year or \
                            contract.contract_end.year < year or \
                    (contract.contract_begin.year == year and contract.contract_begin.month > month) or \
                    (contract.contract_end.year == year and contract.contract_end.month < month):
                raise ValidationError("Invalid workLog (shouldn't happen)")
            workL = WorkLog.objects.get(contract=contract, month=month, year=year)
        except ObjectDoesNotExist:
            workL = WorkLog()
            workL.month = month
            workL.year = year
            workL.contract = contract
            workL.save()
        return workL

    def calc_over_work(self):
        over = 0.0
        lastLog = None
        lastMonth = self.month - 1;
        lastYear = self.year
        if lastMonth == 0:
            lastMonth = 12
            lastYear = lastYear - 1
        try:
            lastLog = self.getWorkLog(self.contract, lastMonth, lastYear)
        except ValidationError:
            pass
        if not lastLog == None:
            lastLogCalc = lastLog.calcHours()
            over = (lastLogCalc - self.contract.hours)
        return over

    def calcHours(self, withOver=True):
        workSum = float(round(self.contract.vacation / 12.0))
        if withOver:
            workSum += self.calc_over_work()
        logs = self.worktime_set.all()
        for l in logs:
            workSum += l.hours
        return workSum


class WorkTime(models.Model):
    work_log = models.ForeignKey(WorkLog)
    hours = models.FloatField(validators=[MinValueValidator(0)])
    pause = models.PositiveIntegerField(default=0)
    begin = models.DateTimeField('Start')
    end = models.DateTimeField('Ende')
    activity = models.CharField(max_length=200)

    def getWorkLog(self, contract, month, year):
        try:
            if contract.contract_begin.year > year or \
                            contract.contract_end.year < year or \
                    (contract.contract_begin.year == year and contract.contract_begin.month > month) or \
                    (contract.contract_end.year == year and contract.contract_end.month < month):
                raise ValidationError("Invalid workLog (shouldn't happen)")
            workL = WorkLog.objects.get(contract=contract, month=month, year=year)
            workSum = workL.calcHours()
        except ObjectDoesNotExist:
            workL = WorkLog()
            workL.month = month
            workL.year = year
            workL.contract = contract
            workL.save()
        return workL

    def getNextWorkLog(self, contract, month, year):
        nextMonth = month + 1
        nextYear = year
        if nextMonth > 12:
            nextMonth = 1
            nextYear += 1
        return self.getWorkLog(contract, nextMonth, nextYear)

    def clean_fields(self, year=-1, month=-1):
        super(WorkTime, self).clean_fields()
        startStamp = time.mktime(self.begin.timetuple())
        endStamp = time.mktime(self.end.timetuple())
        contract = self.work_log.contract
        if contract.contract_begin.year > year or \
                        contract.contract_end.year < year or \
                (contract.contract_begin.year == year and contract.contract_begin.month > month) or \
                (contract.contract_end.year == year and contract.contract_end.month < month):
            raise ValidationError("Date out of contract.")
        if self.begin.weekday() > 4:
            raise ValidationError("You can only work from Mon to Fri.")
        if self.begin.hour < 6 or self.end.hour > 20 or (self.end.hour == 20 and self.end.minute > 0):
            raise ValidationError("You can only work at daytime (06-20h). Sorry coffee nerds ;(")
        if self.end.hour - self.begin.hour - int(self.pause) > 10:
            raise ValidationError("You can only work 10 hours a day.")
        if self.end.hour - self.begin.hour > 6 and int(self.pause) < 1:
            raise ValidationError("You have to make a break of at least 1 hour.")
        if startStamp >= endStamp:
            raise ValidationError(
                'The start time have to be before the end time. In case of a flux capacitor incident please contact the technical support.')
        if (int(self.pause) * 60 * 60) >= endStamp - startStamp:
            raise ValidationError("Such error, many pause!")
        if (self.hours == 0):
            raise ValidationError("Worktime caped to 0.")
        if self.work_log.calcHours() + self.hours > contract.hours:
            if (
                            month == contract.contract_end.month and year == contract.contract_end.year) or self.work_log.calcHours() + self.hours > round(
                        contract.hours * 1.5):
                raise ValidationError("Max. monthly worktime exceeded!")


class FixedWorkDustActivity(models.Model):
    contract = models.ForeignKey(Contract)
    description = models.CharField(max_length=200)
    avg_length = models.IntegerField()
    start = models.TimeField('Start')
    week_day = models.PositiveIntegerField(validators=[MaxValueValidator(4)])


class FillerWorkDustActivity(models.Model):
    contract = models.ForeignKey(Contract)
    description = models.CharField(max_length=200)
    avg_length = models.FloatField(validators=[MinValueValidator(0)])
