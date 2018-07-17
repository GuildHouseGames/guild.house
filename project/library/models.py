# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import requests
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from project import utils
from taggit.managers import TaggableManager

from . import querysets


def get_current_site():
    try:
        return Site.objects.get_current().pk
    except Site.DoesNotExist:
        pass


BGG_JSON_URL = 'https://bgg-json.azurewebsites.net/thing/{bgg_id}'


@python_2_unicode_compatible
class Category(models.Model):

    name = models.CharField(max_length=200)

    title = models.CharField(max_length=200, blank=True, default='')

    heading = models.CharField(max_length=200, blank=True, default='')

    featured_content = models.TextField(blank=True, default='')

    content = models.TextField(blank=True, default='')

    meta_description = models.CharField(max_length=200, blank=True, default='')

    is_enabled = models.BooleanField('enabled', db_index=True, default=True)

    is_featured = models.BooleanField('featured', db_index=True, default=False)

    site = models.ForeignKey('sites.Site', default=get_current_site,
                             related_name='library_categories',
                             on_delete=models.PROTECT)

    slug = models.SlugField()

    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    updated_at = models.DateTimeField(auto_now=True, editable=False)

    objects = querysets.QuerySet.as_manager()

    class Meta(object):
        ordering = ['name']
        unique_together = ['site', 'slug']
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('library:category_detail', kwargs={'slug': self.slug})

    def is_active(self):
        return self in self.__class__.objects.filter(pk=self.pk).active()
    is_active.boolean = True
    is_active.short_description = 'active'

    def save(self, *args, **kwargs):
        if not self.slug:
            queryset = self.__class__.objects.filter(site=self.site)
            self.slug = utils.generate_unique_slug(self.name, queryset)
        return super(Category, self).save(*args, **kwargs)


@python_2_unicode_compatible
class Game(models.Model):

    name = models.CharField(max_length=200)

    categories = models.ManyToManyField(
        'library.Category', related_name='games', related_query_name='game')

    expansion_for = models.ForeignKey(
        'self', related_name='expansions', related_query_name='expansion',
        blank=True, null=True, on_delete=models.PROTECT)

    featured_image = models.ImageField(max_length=1024,
                                       upload_to='games_featured',
                                       blank=True, default='')

    publisher = models.CharField(max_length=200, blank=True, default='')

    boardgamegeek_id = models.PositiveIntegerField(blank=True, null=True)

    boardgamegeek_rank = models.PositiveIntegerField(blank=True, null=True)

    boardgamegeek_img = models.CharField(
        max_length=512, blank=True, default='')

    complexity = models.FloatField(blank=True, null=True)

    minimum_players = models.PositiveIntegerField(blank=True, null=True)

    maximum_players = models.PositiveIntegerField(blank=True, null=True)

    minimum_playtime = models.PositiveIntegerField(
        blank=True, null=True, help_text='Duration in minutes')

    maximum_playtime = models.PositiveIntegerField(
        blank=True, null=True, help_text='Duration in minutes')

    year_published = models.PositiveIntegerField(blank=True, null=True)

    title = models.CharField(max_length=200, blank=True, default='')

    heading = models.CharField(max_length=200, blank=True, default='')

    featured_content = models.TextField(blank=True, default='')

    content = models.TextField(blank=True, default='')

    related = models.ManyToManyField(
        'library.Game',
        blank=True,
    )

    tags = TaggableManager(blank=True)

    meta_description = models.CharField(max_length=200, blank=True, default='')

    is_enabled = models.BooleanField('enabled', db_index=True, default=True)

    is_featured = models.BooleanField('featured', db_index=True, default=False)

    site = models.ForeignKey('sites.Site', default=get_current_site,
                             related_name='library_games',
                             on_delete=models.PROTECT)

    slug = models.SlugField()

    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    updated_at = models.DateTimeField(auto_now=True, editable=False)

    objects = querysets.QuerySet.as_manager()

    class Meta(object):
        ordering = ['name']
        unique_together = ['site', 'slug']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('library:game_detail', kwargs={'slug': self.slug})

    def is_active(self):
        return self in self.__class__.objects.filter(pk=self.pk).active()
    is_active.boolean = True
    is_active.short_description = 'active'

    def is_expansion(self):
        return bool(self.expansion_for)
    is_expansion.boolean = True
    is_expansion.short_description = 'expansion'

    def save(self, *args, **kwargs):
        if not self.slug:
            queryset = self.__class__.objects.filter(site=self.site)
            self.slug = utils.generate_unique_slug(self.name, queryset)

        # Normalise playtime/players: ensure just single "minimum" if not both.

        if self.maximum_playtime and not self.minimum_playtime \
           or self.maximum_playtime == self.minimum_playtime:
            self.minimum_playtime = self.maximum_playtime
            self.maximum_playtime = None

        if self.maximum_players and not self.minimum_players \
           or self.maximum_players == self.minimum_players:
            self.minimum_players = self.maximum_players
            self.maximum_players = None

        return super(Game, self).save(*args, **kwargs)

    def autopopulate_bgg_complexity(self):
        bgg_get = requests.get('https://boardgamegeek.com/boardgame/{}'.format(
            self.boardgamegeek_id))
        location_key = 'boardgameweight":{"averageweight":'
        bgg_content = str(bgg_get.content)
        weight_location = bgg_content.find(location_key)
        weight_location_start = weight_location+len(location_key)
        weight_location_end = weight_location_start + \
            bgg_content[weight_location_start:].find(',')
        self.complexity = bgg_content[
            weight_location_start:weight_location_end]
        self.save()

    def autopopulate_bgg_json(self, bgg_id=None, update_name=True):
        """ This method will create a `Game` object with details provided from
        boardgamegeek, if `self.boardgamegeek_id` """

        if not self.boardgamegeek_id:
            raise ValidationError("No boardgamegeek_id provided. Use method `Game.create_from_bgg_id(bgg_id)`.")  # noqa
        else:
            # See official API here:
            # https://boardgamegeek.com/wiki/page/BGG_XML_API2
            # Note: not using this though. Using a different variant.
            # Using this wrapper rather than the official because JSON
            # is simpler.
            # https://bgg-json.azurewebsites.net/

            this_game = requests.get(
                BGG_JSON_URL.format(bgg_id=self.boardgamegeek_id))

            if not this_game.status_code == 200:
                raise ValidationError("boardgamegeek_id not working")

            # Optional to update name, as we may want to manually set our
            # own name and don't want to fix every time.
            if update_name:
                self.name = this_game.json()['name']

            self.title = this_game.json()['name']
            self.maximum_players = this_game.json()['maxPlayers']
            self.minimum_players = this_game.json()['minPlayers']
            self.minimum_playtime = this_game.json()['playingTime']
            self.minimum_playtime = this_game.json()['playingTime']
            self.year_published = this_game.json()['yearPublished']
            self.boardgamegeek_rank = this_game.json()['rank']
            self.boardgamegeek_img = this_game.json()['image']
            self.content = this_game.json()['description']

            self.save()

    @classmethod
    def create_from_bgg_id(cls, bgg_id):
        "This method will create a `Game` object if provided with a bgg_id."
        new_game = cls()
        new_game.boardgamegeek_id = bgg_id
        new_game.autopopulate_bgg_json()
        new_game.autopopulate_bgg_complexity()
        return new_game
