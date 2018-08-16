# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from .forms import CategoryAdminForm, GameAdminForm
from .models import Category, Game, GameInLibrary, GameRelated, Series
from django.contrib import admin


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    fieldsets = [
        (None, {'fields': ['name', 'slug', 'featured_content',
                           'content', 'meta_description']}),
        ('Publishing', {'fields': ['title', 'heading',
                                   'is_enabled', 'is_featured',
                                   'site', ('created_at', 'updated_at')],
                        'classes': ['collapse']}),
    ]

    form = CategoryAdminForm

    list_display = ['name', 'get_url', 'is_active', 'is_featured']

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


@admin.register(GameInLibrary)
class GameInLibraryAdmin(admin.ModelAdmin):

    model = GameInLibrary


class GameInLibraryInline(admin.TabularInline):

    model = GameInLibrary

    fields = ['location', 'is_broken', 'is_lost',
              'added_at', 'removed_at', 'uid', 'notes']


class GameRelatedInline(admin.TabularInline):

    model = GameRelated

    fk_name = 'game'


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):

    fieldsets = [
        (None, {'fields': [
            'name', 'categories', 'series', 'expansion_for',
            'publisher', 'complexity',
            ('minimum_players', 'maximum_players'),
            ('minimum_playtime', 'maximum_playtime'),
            # 'related',
        ]}),
        ('Scraped', {
            'fields': [
                'boardgamegeek_id', 'boardgamegeek_rank',
                'boardgamegeek_img', 'publisher',
                'year_published',
            ],
            'classes': ['collapse']
        }),
        ('Content', {'fields': [
            'title', 'heading', 'featured_content',
            'featured_image', 'content',
            'meta_description'
        ]}),
        ('Publishing', {
            'fields': [
                'is_enabled', 'is_featured', 'site', 'slug',
                'tags', ('created_at', 'updated_at')
            ],
            'classes': ['collapse']}
         ),
    ]

    form = GameAdminForm

    list_display = [
        'name',
        'is_new',
        'is_featured',
        'display_categories',
        'display_copies',
        'display_minimum_players',
        'display_maximum_players',
        'complexity'
    ]

    def display_minimum_players(self, obj):
        return obj.minimum_players
    display_minimum_players.short_description = "min"

    def display_maximum_players(self, obj):
        return obj.maximum_players
    display_maximum_players.short_description = "max"

    list_filter = [
        'is_enabled',
        'is_featured',
        'categories',
        'minimum_players',
        'maximum_players',
    ]

    list_editable = ['is_new', 'is_featured']

    prepopulated_fields = {'slug': ['name']}

    readonly_fields = ['created_at', 'updated_at']

    search_fields = ['name']

    inlines = [GameInLibraryInline, GameRelatedInline]

    def display_categories(self, obj):
        return ", ".join([x.name for x in obj.categories.all()])
    display_categories.short_description = 'Categories'

    def display_related(self, obj):
        return ", ".join([x.related.name for x in obj.gamerelated_set.all()])
    display_related.short_description = 'Related'

    def display_copies(self, obj):
        return "{} <a href='/admin/library/gameinlibrary/add/'>+</a>".format(
            GameInLibrary.objects.filter(game=obj).count())
    display_copies.short_description = 'Live Copies'
    display_copies.allow_tags = True
