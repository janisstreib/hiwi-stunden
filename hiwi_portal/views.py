from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

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
