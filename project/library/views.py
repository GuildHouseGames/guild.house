# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.shortcuts import get_object_or_404
from django.views import generic
from .models import Category, Game


class GameHome(generic.base.TemplateView):

    template_name = "library/home.html"

    def get_context_data(self, *args, **kwargs):
        data = super(GameHome, self).get_context_data(*args, **kwargs)
        data['categories_list'] = Category.objects.filter(is_enabled=True)
        data['popular_games'] = Game.objects.filter(is_featured=True)
        data['new_games'] = Game.objects.filter(is_new=True)
        return data


class CategoryListView(generic.ListView):

    model = Category

    def get_queryset(self, *args, **kwargs):
        queryset = super(CategoryListView, self).get_queryset(*args, **kwargs)
        return queryset.current_site().active()


class GameListView(generic.ListView):

    model = Game


class GameListViewByCategory(generic.ListView):

    model = Game
    template_name = "library/game_list_by_category.html"

    def get_category(self):
        if not hasattr(self, '_category'):
            self._category = get_object_or_404(
                Category.objects.current_site().active(),
                slug=self.kwargs.get('slug'))
        return self._category

    def get_context_data(self, *args, **kwargs):
        context_data = super(GameListViewByCategory,
                             self).get_context_data(*args, **kwargs)
        context_data.update({'category': self.get_category()})
        return context_data

    def get_queryset(self, *args, **kwargs):
        queryset = super(GameListViewByCategory,
                         self).get_queryset(*args, **kwargs)
        queryset = queryset.filter(categories=self.get_category())
        return queryset.current_site().active()


class GameDetailView(generic.DetailView):

    model = Game

    def get_queryset(self, *args, **kwargs):
        queryset = super(GameDetailView, self).get_queryset(*args, **kwargs)
        return queryset.current_site().active()


class GameDetailMenuView(generic.DetailView):

    model = Game
    template_name = 'library/game_detail_menu.html'
