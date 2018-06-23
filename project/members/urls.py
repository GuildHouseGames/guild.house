# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.conf.urls import include, url
from django.contrib.auth.decorators import permission_required
from django.urls import reverse_lazy
from django.views.generic.base import RedirectView

from . import views

MEMBERS_PERMISSION_REQUIRED = 'members.can_change_member'


urls = [

    url(r'^$',
        RedirectView.as_view(url=reverse_lazy('members:member_form')),
        name='member_new_redirect'),

    url(r'^add/$',
        RedirectView.as_view(url=reverse_lazy('members:member_form')),
        name='member_add_redirect'),

    url(r'^new/$',
        views.member_create_view,
        name='member_form'),

    url(r'^success/',
        views.TemporaryMemberSuccessView.as_view(),
        name='temporarymember_success_view'),

    url(r'^approve/',
        permission_required(MEMBERS_PERMISSION_REQUIRED)(
            views.member_approval_view,
        ),
        name='member_approval'),

    url(r'^import/$',
        permission_required(MEMBERS_PERMISSION_REQUIRED)(
            views.import_view
        ),
        name='members_import'),

    url(r'^list/$',
        permission_required(MEMBERS_PERMISSION_REQUIRED)(
            views.MemberListView.as_view(),
        ),
        name='member_list'),

    url(r'^\+/(?P<number>\d+)$',
        views.member_detail_view,
        name='member_detail'),
]

urlpatterns = [url(r'^', include(urls, namespace='members'))]
