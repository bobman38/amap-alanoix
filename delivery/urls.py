from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='start'),
    url(r'^delivery$', views.home, name='home'),
    url(r'^delivery/(?P<deliverydate_id>[0-9]+)/addme$', views.addme, name='addme'),
    url(r'^delivery/(?P<deliverydate_id>[0-9]+)/removeme$', views.removeme, name='removeme'),
    url(r'^delivery/(?P<deliverydate_id>[0-9]+)/detail$', views.detail, name='detail'),
    url(r'^delivery/edit/(?P<contract_id>[0-9]+)$', views.contractedit, name='contract_edit'),
    url(r'^delivery/view/(?P<contract_id>[0-9]+)$', views.contractview, name='contract_view'),
    url(r'^delivery/view/(?P<contract_id>[0-9]+)/next$', views.contractviewnext, name='contract_view_next'),
    url(r'^delivery/editaccount/(?P<contract_id>[0-9]+)$', views.contracteditaccount, name='contract_edit_account'),
    url(r'^delivery/editaccount/(?P<contract_id>[0-9]+)/add$', views.addfamilytocontract, name='addfamilytocontract'),
    url(r'^delivery/manage/setorder$', views.setorder, name='setorder'),
    url(r'^delivery/manage/setmembershipinfo$', views.setmembershipinfo, name='setmembershipinfo'),
    url(r'^manager$', views.manager, name='manager'),
    url(r'^users$', views.list_users, name='list_users'),
    url(r'^producers$', views.list_producers, name='list_producers'),
]
