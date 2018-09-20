# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from . import views
from django.conf.urls import include, url
from django.contrib.auth.decorators import permission_required

BOOKINGS_PERMISSION_REQUIRED = 'bookings.change_booking'


urls = [

    url(r'^show/numbers/$',
        permission_required(BOOKINGS_PERMISSION_REQUIRED)(
            views.BookingListNumView.as_view()
        ),
        name='booking_list_num'),

    url(r'^show/$',
        permission_required(BOOKINGS_PERMISSION_REQUIRED)(
            views.BookingListView.as_view()
        ),
        name='booking_list'),

    url(r'^form/$',
        permission_required(BOOKINGS_PERMISSION_REQUIRED)(
            views.FormView.as_view(),
        ),
        name='booking_default_form'),

    url(r'^post/$',
        permission_required(BOOKINGS_PERMISSION_REQUIRED)(
            # views.PostView.as_view(),
            views.post_view
        ),
        name='booking_default_post'),

    url(r'^show/(?P<page>\d+)$',
        permission_required(BOOKINGS_PERMISSION_REQUIRED)(
            views.BookingListView.as_view()
        ),
        name='booking_list_pagination'),

    url(r'^cancelled/$',
        permission_required(BOOKINGS_PERMISSION_REQUIRED)(
            views.BookingCancelledView.as_view()
        ),
        name="booking_list_cancelled"),

    url(r'^future/$',
        permission_required(BOOKINGS_PERMISSION_REQUIRED)(
            views.BookingFutureView.as_view()
        ),
        name='booking_future'),

    url(r'^today/$',
        permission_required(BOOKINGS_PERMISSION_REQUIRED)(
            views.BookingTodayArchiveView.as_view()
        ),
        name="booking_today"),

    url(r'^(?P<year>\d{4})/$',
        permission_required(BOOKINGS_PERMISSION_REQUIRED)(
            views.BookingYearArchiveView.as_view()
        ),
        name="booking_year"),

    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$',
        permission_required(BOOKINGS_PERMISSION_REQUIRED)(
            views.BookingMonthArchiveView.as_view()
        ),
        name="booking_month"),

    url(r'^(?P<year>\d{4})/week/(?P<week>\d+)/$',
        permission_required(BOOKINGS_PERMISSION_REQUIRED)(
            views.BookingWeekArchiveView.as_view()
        ),
        name="booking_week"),

    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
        permission_required(BOOKINGS_PERMISSION_REQUIRED)(
            views.BookingDayArchiveView.as_view()
        ),
        name="booking_day"),

    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>[\w-]+)$',
        permission_required(BOOKINGS_PERMISSION_REQUIRED)(
            views.BookingDetailView.as_view()
        ),
        name='booking_detail'),

    url(r'^$',
        views.BookingCreateView.as_view(),
        name="booking_add"),

    url(r'^time/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
        views.BookingTimeView.as_view(),
        name='booking_times'),

    # Used to save some horrible frontend code to reformat date on
    # bookings form.
    url(r'^time/(?P<day>\d{2})/(?P<month>\d{2})/(?P<year>\d{4})/$',
        views.BookingTimeView.as_view(),
        name='booking_times_reversed'),

    url(r'^b/(?P<code>[\w-]+)/run/$',
        views.BookingRunView.as_view(),
        name="booking_run"),

    url(r'^b/(?P<code>[\w-]+)/success/$',
        views.BookingSuccessView.as_view(),
        name="booking_success"),

    url(r'^b/(?P<code>[\w-]+)/$',
        views.BookingUpdateView.as_view(),
        name="booking_update"),

]

urlpatterns = [url(r'^', include(urls, namespace='bookings'))]
