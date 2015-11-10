from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from models import Contract
from datetime import datetime

@login_required
def index(request):
    context = {"user":request.user}
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


@login_required
def contractAdd(request):
    user = request.user
    context = {"user":user}
    try:
        if request.method == 'POST':
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
        context['post'] = 'y'
    except ValidationError as v:
        context['error'] = v.messages
        print(v)
    except ValueError as v:
        context['error'] = [v.message]
    return render(request, 'contract_add.html', context)
