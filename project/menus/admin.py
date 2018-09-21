# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from .forms import MenuTypeAdminForm
from .models import MenuType, MenuImage, ItemType, Item
from django.contrib import admin


class MenuImageInline(admin.TabularInline):

    model = MenuImage
    extra = 0


@admin.register(MenuType)
class MenuTypeAdmin(admin.ModelAdmin):

    form = MenuTypeAdminForm
    list_display = ['title', 'order',  'updated_at']
    list_editable = ['order']

    inlines = [
        MenuImageInline,
    ]
