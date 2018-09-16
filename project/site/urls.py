# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from . import views
from django.conf.urls import include, url


urls = [

    url(r'^$',
        views.HomepageDetailView.as_view(),
        name='home'),

    url(r'^detail/$', views.HomepageDetailView.as_view(),
        name='homepage_detail'),

]


urlpatterns = [url(r'^', include(urls, namespace='site'))]
