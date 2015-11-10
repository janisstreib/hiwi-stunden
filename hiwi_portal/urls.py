from django.conf.urls import url

from . import views
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

urlpatterns = [
    url(r'^profile/contract/add/$', views.contractAdd, name='contractAdd'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^$', views.index, name='index'),
]
