# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from models import Contract, WorkLog, WorkTime, FillerWorkDustActivity, FixedWorkDustActivity
from datetime import datetime, timedelta
from calendar import monthrange
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
import tempfile
import shutil
import configparser
import time
from django.contrib.auth import logout
from subprocess import Popen
FORM = ""

def getMilogPath():
    global FORM
    if FORM:
        return FORM
    config = configparser.ConfigParser()
    config.read("config.ini")
    try:
        FORM = config.get("formgen", "milog_path")
        return FORM
    except configparser.NoOptionError as e:
        print ("Missing configuartion! ", e)
        exit(1)

#TODO: In ordentlich im model
def calcHours(worklog):
    workSum = worklog.overWork + round(worklog.contract.vacation/12.0)
    logs = worklog.worktime_set.all()
    for l in logs:
        workSum += l.hours
    return workSum

def getWorkLog(contract, month, year):
    try:
        if contract.contract_begin.year > year or \
        contract.contract_end.year < year or \
        (contract.contract_begin.year == year and contract.contract_begin.month > month) or \
        (contract.contract_end.year == year and contract.contract_end.month < month):
            raise ValidationError("Invalid workLog (shouldn't happen)")
        workL = WorkLog.objects.get(contract=contract, month=month, year=year)
        workSum = calcHours(workL)
    except ObjectDoesNotExist:
        workL = WorkLog()
        workL.month = month
        workL.year = year
        workL.contract = contract
        workL.save()
    return workL

def getNextWorkLog(contract, month, year):
    nextMonth = month+1
    nextYear = year
    if nextMonth > 12:
        nextMonth = 1
        nextYear +=1
    return getWorkLog(contract, nextMonth, nextYear)

@login_required
def index(request):
    user = request.user
    context = {"user":user}
    contracts = user.contract_set.all()
    now = datetime.now()
    month = now.month
    year = now.year
    context['year'] = year
    context['month'] = month
    if request.method == 'GET':
        if request.GET.get('month') and request.GET.get('year'):
            if int(request.GET['month']) > 12 or int(request.GET['month']) < 1:
                raise ValidationError("Invalid month.")
            if int(request.GET['year']) > year+2 or int(request.GET['year']) < year-2:
                raise ValidationError("Invalid year.")
            month = int(request.GET['month'])
            year = int(request.GET['year'])
            context['year'] = year
            context['month'] = month
    if request.method == 'POST':
        if request.POST.get('month') and request.POST.get('year'):
            if int(request.POST['month']) > 12 or int(request.POST['month']) < 1:
                raise ValidationError("Invalid month.")
            if int(request.POST['year']) > year+2 or int(request.POST['year']) < year-2:
                raise ValidationError("Invalid year.")
            month = int(request.POST['month'])
            year = int(request.POST['year'])
            context['year'] = year
            context['month'] = month
        if request.POST.get("contract_id"):
            try:
                contract = Contract.objects.get(id=request.POST["contract_id"])
                wt = WorkTime()
                wt.activity = request.POST['activity']
                #wt.hours = request.POST['work']
                wt.pause = request.POST['pause']
                if not wt.pause:
                    wt.pause = 0
                start = request.POST['date'] + "  " + request.POST['start']
                start = datetime.strptime(start, "%Y-%m-%d %H:%M")
                end = request.POST['date'] + "  " + request.POST['end']
                end = datetime.strptime(end, "%Y-%m-%d %H:%M")
                year = start.year
                month = start.month
                if contract.contract_begin.year > year or \
                contract.contract_end.year < year or \
                (contract.contract_begin.year == year and contract.contract_begin.month > month) or \
                (contract.contract_end.year == year and contract.contract_end.month < month):
                        raise ValidationError("Date out of contract.")
                startStamp = time.mktime(start.timetuple())
                endStamp = time.mktime(end.timetuple())
                wLog = WorkLog.objects.get(contract=contract, month=month, year=year)
                if start.weekday() > 4:
                    raise ValidationError("You can only work from Mon to Fri.")
                if start.hour < 6 or end.hour > 20 or (end.hour==20 and end.minute > 0):
                    raise ValidationError("You can only work at daytime (06-20h). Sorry coffee nerds ;(")
                if end.hour - start.hour - int(wt.pause) > 10:
                    raise ValidationError("You can only work 10 hours a day.")
                if end.hour - start.hour > 6 and int(wt.pause) < 1:
                    raise ValidationError("You have to make a break of at least 1 hour.")
                if startStamp >= endStamp:
                    raise ValidationError('The start time have to be before the end time. In case of a flux capacitor incident please contact the technical support.')
                if (int(wt.pause)*60*60) >= endStamp-startStamp:
                    raise ValidationError("Such error, many pause!")
                wt.hours = round(((endStamp-startStamp)-int(wt.pause)*60*60)/60/60)
                if(wt.hours == 0):
                    raise ValidationError("Worktime caped to 0.")
                if calcHours(wLog)+wt.hours > contract.hours:
                    if (month == contract.contract_end.month and year == contract.contract_end.year) or calcHours(wLog)+wt.hours > round(contract.hours*1.5):
                        raise ValidationError("Max. monthly worktime exceeded!")
                    else:
                        nextLog = getNextWorkLog(contract, month, year)
                        nextLog.overWork = nextLog.overWork + calcHours(wLog)+wt.hours - contract.hours
                        nextLog.save()

                wt.work_log = wLog
                wt.end = end
                wt.begin = start
                wt.clean_fields()
                wt.save()
            except ObjectDoesNotExist as v:
                context['error'] = [v.message]
            except ValueError as v:
                context['error'] = [v.message]
            except ValidationError as v:
                context['error'] = v.messages
            context['post'] = 'y'
            context['posted_contract'] = int(request.POST['contract_id'])
            context['postdata'] = request.POST
    month = context['month']
    year = context['year']
    ctracs = []
    for c in contracts:
        if c.contract_begin.year > year or \
        c.contract_end.year < year or \
        (c.contract_begin.year == year and c.contract_begin.month > month) or \
        (c.contract_end.year == year and c.contract_end.month < month):
            continue

        workL = getWorkLog(c, month, year)
        workSum = calcHours(workL)
        c.cw=workL
        c.cSum = workSum
        c.partVac = int(round(workL.contract.vacation/12.0))
        if c.hours*1.5-workSum <= c.hours*1.5-c.hours:
            c.critSum = True
        ctracs.append(c)
    context['contracts'] = ctracs
    years = []
    for i in range(-2, 3):
        years.append(datetime.now().year+i)
    context['years'] = years
    return render(request, 'hiwi_portal.html', context)


@login_required
def profile(request):
    user = request.user
    context = {"user":user}
    try:
        if request.method == 'POST':
            if not request.POST["data"] == None:
                    user.phone_number = request.POST['phone']
                    user.private_email = request.POST['private_email']
                    user.clean_fields()
                    if 'private_notif' in request.POST:
                        if not request.POST['private_email']:
                            raise ValidationError("A private E-Mail adress is required to get notified to your private E-Mail adress.")
                        user.notify_to_private = True
                    else:
                        user.notify_to_private = False
                    user.save()
            context['post'] = 'y'
    except ValidationError as v:
        context['error'] = v.messages
    return render(request, 'profile.html', context)

def faq(request):
    return render(request, 'faq.html', {})

@login_required
def contractAdd(request):
    user = request.user
    context = {"user":user}
    try:
        if request.method == 'POST':
            context['post'] = 'y'
            contract = Contract()
            contract.department = request.POST['institute']
            contract.user = user
            contract.personell_number = request.POST['personell_id']
            cStart = request.POST['contract_start']
            cEnd = request.POST['contract_end']
            cStart = datetime.strptime(cStart, "%Y-%m-%d")
            cEnd = datetime.strptime(cEnd, "%Y-%m-%d")
            contract.contract_begin = cStart
            contract.contract_end = cEnd
            contract.personell = request.POST['dp']
            contract.hours = request.POST['work_hours']
            contract.payment = request.POST['payment']
            contract.vacation = round((int(contract.hours) *20*3.95)/85.0)
            contract.clean_fields()
            contract.save()
            return redirect("/profile")

    except ValidationError as v:
        context['error'] = v.messages
        print(v)
    except ValueError as v:
        context['error'] = [v.message]
    context['postdata'] = request.POST
    return render(request, 'contract_add.html', context)

@login_required
def printView(request, contract, month, year):
    user = request.user
    contract = Contract.objects.get(id=int(contract), user=user)
    workL = WorkLog.objects.get(month=int(month),year=int(year), contract=contract)
    response = HttpResponse(content_type='application/pdf')

    out = tempfile.mkdtemp()
    templ = open(getMilogPath()+"/milog_form_placehold.tex", "r")
    templEnd = open(out+'/h.tex', "w+")
    templR = templ.read().decode("utf-8")
    templ.close()
    templR = templR.replace("{!name}", user.lastname +", "+user.firstname)
    templR = templR.replace("{!personell_number}", str(contract.personell_number))
    if(contract.personell == "UB"):
        templR = templR.replace("{!gf}", "")
        templR = templR.replace("{!ub}", "checked,")
    else:
        templR = templR.replace("{!gf}", "checked,")
        templR = templR.replace("{!ub}", "")
    templR = templR.replace("{!contract_hours}", str(contract.hours))
    templR = templR.replace("{!contract_pay}", str(contract.payment))
    templR = templR.replace("{!my}", month+"/"+year)
    rows = ""
    for t in  workL.worktime_set.all():
        rows += "%s & %s & %s & %s & %s & %d\\\\ \hline\n" % (t.activity,
            t.start.strftime("%d.%m.%y") ,
            t.begin.strftime("%H:%M"),
            t.end.strftime("%H:%M"),
            str(t.pause)+":00",
            t.hours)
    endSum = calcHours(workL)
    templR = templR.replace("{!rows}", rows)
    templR = templR.replace("{!sum}", str(int(endSum)))
    templR = templR.replace("{!overwork}", str(workL.overWork))
    templR = templR.replace("{!vacation}", str(int(round(workL.contract.vacation/12.0))))
    overNext = endSum - contract.hours
    if overNext < 0:
        overNext = 0
    templR = templR.replace("{!overworknext}", str(int(overNext)))
    templEnd.write(templR.encode("utf-8"))
    templEnd.close()
    p = Popen(['pdflatex', '-output-directory='+out, out+'/h.tex', '-interaction nonstopmode', '-halt-on-error', '-file-line-error'], cwd=getMilogPath())
    p.wait()
    f = open(out+'/h.pdf', 'r')
    response.write(f.read())
    f.close()
    shutil.rmtree(out)
    return response

@login_required
def delete_profile(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        return redirect("/logout")
    return redirect("/profile")

@login_required
def delete_contract(request):
    contr = Contract(user=request.user, id=int(request.path_info.split("/")[3]))
    contr.delete()
    return redirect("/profile/")

@login_required
def delete_work(request):
    wt = WorkTime.objects.get(id=int(request.path_info.split("/")[2]))
    if wt.work_log.contract.user == request.user:
        cid= str(wt.work_log.contract.id)
        month = str(wt.work_log.month)
        year = str(wt.work_log.year)
        wt.delete()
    return redirect("/?month="+month+"&year="+year+"#"+cid)

@login_required
def work_dust(request):
    user = request.user
    user.work_dusted = True
    user.save()
    return redirect("/")

@login_required
def wd_manage_fill(request):
    user = request.user
    c = Contract.objects.get(id=int(request.POST['contract']), user=user)
    f = FillerWorkDustActivity()
    f.contract = c
    f.description = request.POST['description']
    f.avg_length = request.POST['dur']
    f.clean_fields()
    f.save()
    return redirect("/profile")

@login_required
def wd_manage_anual(request):
    user = request.user
    c = Contract.objects.get(id=int(request.POST['contract']), user=user)
    f = FixedWorkDustActivity()
    start = request.POST['start']
    f.start = datetime.strptime(start, "%H:%M")
    f.contract = c
    f.week_day = request.POST['weekday']
    f.description = request.POST['description']
    f.avg_length = request.POST['dur']
    f.clean_fields()
    f.save()
    return redirect("/profile")

@login_required
def wd_manage_apply(request, month, year, contract):
    c = Contract.objects.get(id=int(contract), user=request.user)
    month = int(month)
    year= int(year)
    firstDayOfMonth = datetime(year, month, 1, 0, 0, 1, 0).weekday()
    daysInMonth = monthrange(year, month)
    workL = WorkLog.objects.get(contract=c, month=month, year=year)
    #First try apply all anual activities
    anuals = c.fixedworkdustactivity_set.all()
    for a in anuals:
        if a.week_day > firstDayOfMonth:
            anualStep = 2 + a.week_day -firstDayOfMonth
        else:
            anualStep = 2 + 6-firstDayOfMonth+a.week_day
        while anualStep <= daysInMonth[1] and calcHours(workL) +a.avg_length < c.hours:
            wt = WorkTime()
            wt.hours = a.avg_length
            wt.work_log = workL
            if a.avg_length >= 6:
                wt.pause = 1
            else:
                wt.pause = 0
            wt.hours = a.avg_length
            wt.begin =  datetime(year, month, anualStep, a.start.hour, a.start.minute, 0, 0)
            wt.end = wt.begin.replace(hour=wt.begin.hour+wt.pause+wt.hours)
            wt.activity = a.description
            wt.clean_fields()
            wt.save()
            anualStep +=7
    #Then fill with "other" activities
    return redirect("/?month="+str(month)+"&year="+str(year)+"#"+str(c.id))
