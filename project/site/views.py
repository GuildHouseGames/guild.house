# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import date, timedelta
from django.http import Http404
from django.utils import timezone
from django.views import generic
from . import settings
from .models import Homepage, OpeningHours, Slide


class HomeView(generic.TemplateView):

    template_name = "site/home.html"

    def get_context_data(self, *args, **kwargs):
        context_data = super(HomeView, self).get_context_data(
            *args, **kwargs)
        context_data['slide_list'] = Slide.objects.filter(
            is_active=True,
            publish_at__lte=timezone.now(),
        )
        return context_data

    pass


class HoursView(generic.TemplateView):

    template_name = "site/opening_hours.html"

    def get_context_data(self, *args, **kwargs):
        context = super(HoursView, self).get_context_data(*args, **kwargs)

        hours_list, this_list = [], []
        td = timedelta(days=1)
        for day in OpeningHours.objects.filter(
                date__gte=date.today()-td):
            if this_list and day.date-td != this_list[-1].date:
                hours_list.append(this_list)
                this_list = [day]
            else:
                this_list.append(day)
        hours_list.append(this_list)
        context['hours_list'] = hours_list
        return context


class HomepageDetailView(generic.DetailView):

    model = Homepage
    template_name = "site/home.html"

    def get_categories(self):
        return self.object.site.library_categories.featured().active()[
            :settings.HOMEPAGE_CATEGORIES]

    def get_entries(self):
        return self.object.site.blog_entries.featured().active()[
            :settings.HOMEPAGE_ENTRIES]

    def get_context_data(self, *args, **kwargs):
        context_data = super(HomepageDetailView, self).get_context_data(
            *args, **kwargs)
        context_data.update({'category_list': self.get_categories(),
                             'entry_list': self.get_entries(),
                             'game_list': self.get_games()})
        return context_data

    def get_games(self):
        return self.object.site.library_games.featured().active()[
            :settings.HOMEPAGE_GAMES]

    def get_object(self, *args, **kwargs):
        try:
            return Homepage.objects.active().get_current()
        except Homepage.DoesNotExist:
            raise Http404('Homepage does not exist.')
