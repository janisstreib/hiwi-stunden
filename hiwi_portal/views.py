# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from models import Contract, WorkLog, WorkTime
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
import tempfile
import shutil
from subprocess import Popen

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
    ctracs = []
    for c in contracts:
        try:
            workL = WorkLog.objects.get(contract=c, month=month, year=year)
        except ObjectDoesNotExist:
            workL = WorkLog()
            workL.month = month
            workL.year = year
            workL.contract = c
            workL.save()
        c.cw=workL

        ctracs.append(c)
    context['contracts'] = ctracs
    print(contracts)
    if request.method == 'POST':
        try:
            contract = Contract.objects.get(id=request.POST["contract-id"])
            wLog = WorkLog.objects.get(contract=c, month=month, year=year)
            wt = WorkTime()
            wt.work_log = wLog
            wt.activity = request.POST['activity']
            wt.hours = request.POST['work']
            wt.pause = request.POST['pause']
            date = request.POST['date']
            end = request.POST['end']
            start = request.POST['start']
            start = datetime.strptime(start, "%H:%M")
            end = datetime.strptime(end, "%H:%M")
            date = datetime.strptime(date, "%Y-%m-%d")
            wt.end = end
            wt.begin = start
            wt.date = date
            wt.clean_fields()
            wt.save()
        except ObjectDoesNotExist as v:
            context['error'] = [v.message]
        except ValueError as v:
            context['error'] = [v.message]
        except ValidationError as v:
            context['error'] = v.messages
        context['post'] = 'y'

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
            contract.personell_number = request.POST['personell-id']
            cStart = request.POST['contract-start']
            cEnd = request.POST['contract-end']
            cStart = datetime.strptime(cStart, "%Y-%m-%d")
            cEnd = datetime.strptime(cEnd, "%Y-%m-%d")
            contract.contract_begin = cStart
            contract.contract_end = cEnd
            contract.personell = request.POST['dp']
            contract.hours = request.POST['work-hours']
            contract.payment = request.POST['payment']
            contract.clean_fields()
            contract.save()
            redirect("/profile")

    except ValidationError as v:
        context['error'] = v.messages
        print(v)
    except ValueError as v:
        context['error'] = [v.message]
    return render(request, 'contract_add.html', context)

@login_required
def printView(request):
    user = request.user
    pathComp = request.path_info.split("/")
    contract = Contract.objects.get(id=int(pathComp[2]), user=user)
    workL = WorkLog.objects.get(month=int(pathComp[3]),year=int(pathComp[4]), contract=contract)
    print(contract)
    response = HttpResponse(content_type='application/pdf')

    out = tempfile.mkdtemp()
    templ = open("milog-form/milog_form_placehold.tex", "r")
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
    templR = templR.replace("{!my}", pathComp[3]+"/"+pathComp[4])
    rows = ""
    endSum = 0
    for t in  workL.worktime_set.all():
        rows += "%s & %s & %s & %s & %s & %d\\\\ \hline\n" % (t.activity, t.date.strftime("%d.%m.%y") , t.begin, t.end, "", t.hours)
        endSum += t.hours
    templR = templR.replace("{!rows}", rows)
    templR = templR.replace("{!sum}", str(endSum))
    templEnd.write(templR.encode("utf-8"))
    templEnd.close()
    p = Popen(['pdflatex', '-output-directory='+out, out+'/h.tex', '-interaction nonstopmode', '-halt-on-error', '-file-line-error'], cwd='milog-form/')
    p.wait()
    f = open(out+'/h.pdf', 'r')
    response.write(f.read())
    f.close()
    #out.close()
    # It's usually a good idea to set the 'Content-Length' header too.
    # You can also set any other required headers: Cache-Control, etc.
    shutil.rmtree(out)
    return response
