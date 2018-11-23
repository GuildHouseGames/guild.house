# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from .forms import BookingAdminForm
from .models import Booking
from django.contrib import admin


def get_obj_link(obj):
    return "<a href='{0}' target='_blank'>{1}</a>".format(obj.get_absolute_url(), obj.code)


get_obj_link.allow_tags = True
get_obj_link.short_description = "URL"


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    date_hierarchy = 'reserved_date'

    fieldsets = [
        ('Content', {'fields': ['reserved_date', 'reserved_time',
                                'booking_duration', 'name', 'party_size',
                                'status', 'is_cancelled', 'email',
                                'phone', 'notes', 'private_notes']}),
        ('Publishing', {'fields': ['site', ('created_at', 'updated_at')],
                        'classes': ['collapse']}),
    ]

    form = BookingAdminForm

    list_display = ['name', 'party_size', 'reserved_date', 'reserved_time',
                    'service', 'get_status_display', 'phone', 'email', get_obj_link]

    list_filter = ['status', 'service', 'reserved_date', 'reserved_time']

    readonly_fields = ['created_at', 'updated_at']

    search_fields = ['name', 'email', 'notes',
                     'reserved_date', 'user__username']
