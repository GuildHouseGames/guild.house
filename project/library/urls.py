# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required

from . import views


urls = [

    url(r'^$',
        login_required(views.GameHome.as_view()),
        name='game_home'),

    url(r'^categories/$',
        login_required(views.CategoryListView.as_view()),
        name='category_list'),

    url(r'^c/(?P<slug>[\w-]+)/$',
        login_required(views.GameListViewByCategory.as_view()),
        name='category_detail'),

    url(r'^g/(?P<slug>[\w-]+)/$',
        login_required(views.GameDetailView.as_view()),
        name='game_detail'),

    url(r'^menu/(?P<slug>[\w-]+)/$',
        login_required(views.GameDetailMenuView.as_view()),
        name='game_detail_menu'),

    url(r'^add/bgg/$',
        # LOGIN SHOULD ALWAYS BE REQUIRED HERE
        login_required(views.GameAddBGGID.as_view()),
        name='game_bgg_add'),

    url(r'^all/$',
        login_required(views.GameListView.as_view()),
        name='game_all'),
]


urlpatterns = [url(r'^', include(urls, namespace='library'))]
