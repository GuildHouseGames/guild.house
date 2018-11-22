# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required

from . import views
from . import views_maintenance


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

    url(r'^all/$',
        login_required(views.GameListView.as_view()),
        name='game_all'),

    # Maintenance Views

    url(r'^add/bgg/$',
        # LOGIN SHOULD ALWAYS BE REQUIRED HERE
        login_required(views_maintenance.GameAddBGGID.as_view()),
        name='game_bgg_add'),

    url(r'^m/$',
        # LOGIN SHOULD ALWAYS BE REQUIRED HERE
        login_required(views_maintenance.MaintenanceRegister.as_view()),
        name='maintenance_register'),

    url(r'^m/c/$',
        # LOGIN SHOULD ALWAYS BE REQUIRED HERE
        login_required(views_maintenance.CopyRegister.as_view()),
        name='copy_register'),

    url(r'^m/a/$',
        # LOGIN SHOULD ALWAYS BE REQUIRED HERE
        login_required(views_maintenance.MaintenanceRegister.as_view()),
        name='copy_register_add'),


    url(r'^m/(?P<pk>[\d]+)',
        # LOGIN SHOULD ALWAYS BE REQUIRED HERE
        login_required(views_maintenance.MaintainGame.as_view()),
        name='maintain_game'),

    url(r'^m/(?P<pk>[\d]+)/(?P<num>[\d]+)/',
        # LOGIN SHOULD ALWAYS BE REQUIRED HERE
        login_required(views_maintenance.MaintainCopy.as_view()),
        name='maintain_copy'),

    url(r'^m/copy/add',
        # LOGIN SHOULD ALWAYS BE REQUIRED HERE
        login_required(views_maintenance.AddCopy.as_view()),
        name='add_copy'),

]


urlpatterns = [url(r'^', include(urls, namespace='library'))]
