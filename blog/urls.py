# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views
from .models import *

urlpatterns = [
    url(r'^(?P<year>\d{4})/(?P<month>[0-9]+)/(?P<day>[0-9]+)/(?P<slug>[\w-]+)/$',login_required(views.EntryDetail.as_view()),name='blog_entry'),
    url(r'^$',login_required(views.IndexView.as_view()),name='blog'),
    url(r'^addcomment/(?P<entry_id>[0-9]+)$',views.add_comment,name='add_comment'),
    url(r'^new$', login_required(views.EntryCreate.as_view()), name='new')
]
