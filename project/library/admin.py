# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.contrib import admin

from .forms import CategoryAdminForm, GameAdminForm
from .models import (Category, Game, Copy, GameRelated,
                     Series, CopyHistory, Consumable, Issue)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    fieldsets = [
        (None, {'fields': ['name']}),
        ('Content', {'fields': ['title', 'heading', 'featured_content',
                                'content', 'meta_description']}),
        ('Publishing', {'fields': ['is_enabled', 'is_featured', 'site', 'slug',
                                   ('created_at', 'updated_at')],
                        'classes': ['collapse']}),
    ]

    form = CategoryAdminForm

    list_display = ['name', 'is_active', 'is_featured']

    list_filter = ['is_enabled', 'is_featured']

    prepopulated_fields = {'slug': ['name']}

    readonly_fields = ['created_at', 'updated_at']

    search_fields = ['name']

    def get_url(self, obj):
        return "<a target='_blank'  href={}>{}</a>".format(
            obj.get_absolute_url(),
            obj.slug
        )
    get_url.allow_tags = True


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):

    model = Series

    prepopulated_fields = {'slug': ['name']}


class CopyHistoryInline(admin.TabularInline):

    model = CopyHistory


@admin.register(Copy)
class CopyAdmin(admin.ModelAdmin):

    model = Copy

    inlines = [CopyHistoryInline]


class CopyInline(admin.TabularInline):

    model = Copy

    fields = ['location', 'is_dead', 'is_lost',
              'added_at', 'removed_at', 'uid', 'notes']


class GameRelatedInline(admin.TabularInline):

    model = GameRelated

    fk_name = 'game'


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):

    fieldsets = [
        (None, {'fields': ['name', 'categories', 'expansion_for',
                           'publisher', 'complexity',
                           'boardgamegeek_rank', 'year_published',
                           ('minimum_players', 'maximum_players'),
                           ('minimum_playtime', 'maximum_playtime')]}),
        ('Content', {'fields': ['title', 'heading', 'featured_content',
                                'content', 'meta_description']}),
        ('Publishing', {'fields': ['is_enabled', 'is_featured', 'site', 'slug',
                                   'tags', ('created_at', 'updated_at')],
                        'classes': ['collapse']}),
    ]

    form = GameAdminForm

    list_display = ['name', 'complexity',
                    'is_active', 'is_featured', 'is_expansion']

    list_filter = ['is_enabled', 'is_featured']

    prepopulated_fields = {'slug': ['name']}

    readonly_fields = ['created_at', 'updated_at']

    search_fields = ['name']

    inlines = [CopyInline, GameRelatedInline]

    def display_categories(self, obj):
        return ", ".join([x.name for x in obj.categories.all()])
    display_categories.short_description = 'Categories'

    def display_related(self, obj):
        return ", ".join([x.related.name for x in obj.gamerelated_set.all()])
    display_related.short_description = 'Related'

    def display_copies(self, obj):
        return "{} <a href='/admin/library/gameinlibrary/add/'>+</a>".format(
            Copy.objects.filter(game=obj).count())
    display_copies.short_description = 'Live Copies'
    display_copies.allow_tags = True


admin.site.register(Consumable)
admin.site.register(Issue)
