from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='start'),
    url(r'^delivery$', views.home, name='home'),
    url(r'^delivery/(?P<deliverydate_id>[0-9]+)/addme$', views.addme, name='addme'),
    url(r'^delivery/(?P<deliverydate_id>[0-9]+)/removeme$', views.removeme, name='removeme'),
    url(r'^delivery/(?P<deliverydate_id>[0-9]+)/detail$', views.detail, name='detail'),
    url(r'^delivery/manage/(?P<contract_id>[0-9]+)$', views.manage, name='manage'),
    url(r'^delivery/manageaccount/(?P<contract_id>[0-9]+)$', views.manageaccount, name='manageaccount'),
    url(r'^delivery/manage/setorder$', views.setorder, name='setorder'),
    url(r'^delivery/manage/getorder$', views.getorder, name='getorder'),
    url(r'^delivery/manage/getorderalldates$', views.getorderalldates, name='getorderalldates'),
]
