# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from .forms import HomepageAdminForm
from .models import (Homepage, Navigation, OpeningHours, Slide, SlideBanner)
from django.contrib import admin


@admin.register(Homepage)
class HomepageAdmin(admin.ModelAdmin):

    fieldsets = [
        ('Content', {'fields': ['title', 'heading', 'featured_content',
                                'content', 'meta_description']}),
        ('Publishing', {'fields': ['is_enabled', 'site',
                                   ('created_at', 'updated_at')],
                        'classes': ['collapse']}),
    ]

    form = HomepageAdminForm

    list_display = ['__str__', 'is_active']

    readonly_fields = ['created_at', 'updated_at']


@admin.register(Navigation)
class NavigationAdmin(admin.ModelAdmin):

    list_display = ['title', 'url', 'is_active', 'order']

    list_editable = ['order']


@admin.register(OpeningHours)
class OpeningHoursAdmin(admin.ModelAdmin):

    list_display = ['date', 'named_day',
                    'open_time', 'close_time', 'open', 'is_closed', 'note']

    list_editable = ['named_day', 'open_time',
                     'close_time', 'open', 'is_closed', 'note']


class SlideBannerInline(admin.TabularInline):

    model = SlideBanner

    extra = 0


@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):

    model = Slide

    inlines = [SlideBannerInline]
