from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    context = {"user":request.user}
    return render(request, 'hiwi_portal.html', context)
