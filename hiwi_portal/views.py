from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    context = {"user":request.user}
    return render(request, 'hiwi_portal.html', context)


@login_required
def profile(request):
    context = {"user":request.user}
    return render(request, 'profile.html', context)
