from django.conf.urls import url

from . import views
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

urlpatterns = [
    url(r'^profile/contract/[0-9]+/delete$', views.delete_contract, name='contract delete'),
    url(r'^work/[0-9]+/delete$', views.delete_work, name='work delete'),
    url(r'^contract/([0-9]+)/(10|11|12|[1-9])/([0-9]{4})/print/$', views.printView, name='print'),
    url(r'^profile/contract/add/$', views.contractAdd, name='contractAdd'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/delete$', views.delete_profile, name='delete profile'),
    url(r'^profile/work-dust$', views.work_dust, name='workduster'),
    url(r'^profile/work-dust/add/anual$', views.wd_manage_anual, name='wd_manage_anual'),
    url(r'^profile/work-dust/add/fill$', views.wd_manage_fill, name='wd_manage_fill'),
    url(r'^profile/work-dust/apply/(10|11|12|[1-9])/([0-9]{4})/([0-9]+)$', views.wd_manage_apply,
        name='wd_manage_apply'),
    url(r'^profile/work-dust/weekly/([0-9]+)/delete$', views.wd_delete_anual, name='wd_manage_delte'),
    url(r'^profile/work-dust/filler/([0-9]+)/delete$', views.wd_delete_filler, name='wd_manage_delte'),
    url(r'^$', views.index, name='index'),
    url(r'^faq/$', views.faq, name='faq'),
]
