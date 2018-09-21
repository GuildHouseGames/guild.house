# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.contrib.sites.models import Site
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible


def get_current_site():
    try:
        return Site.objects.get_current().pk
    except Site.DoesNotExist:
        pass


MENU_CHOICES = [
    ('food', 'food'),
    ('drinks', 'drinks'),
    ('banquet', 'banquet'),
    ('games', 'games'),
]


@python_2_unicode_compatible
class MenuType(models.Model):

    type = models.CharField(
        max_length=32, choices=MENU_CHOICES, blank=True, default='')

    title = models.CharField(max_length=200, blank=True, default='')

    summary = models.TextField(blank=True, default='')

    order = models.IntegerField(default=0)

    is_enabled = models.BooleanField('enabled', db_index=True, default=True)

    publish_at = models.DateTimeField(db_index=True, default=timezone.now)

    updated_at = models.DateTimeField(auto_now=True, editable=False)

    menu_image = models.ImageField(max_length=1024,
                                   upload_to='menu_image',
                                   blank=True, default='')

    menu_file = models.FileField(max_length=1024,
                                 upload_to='menu_file',
                                 blank=True, default='')

    class Meta(object):
        ordering = ['order', 'pk']
        verbose_name_plural = 'menus'

    def __str__(self):
        return self.title


class MenuImage(models.Model):

    menu = models.ForeignKey('menus.MenuType')

    image = models.ImageField(max_length=1024,
                              upload_to='menu_image',
                              blank=True, default='')

    width = models.CharField(max_length=32, default="100%")


class ItemType(models.Model):

    title = models.CharField(max_length=200, blank=True, default='')


class Item(models.Model):

    title = models.CharField(max_length=200, blank=True, default='')

    description = models.CharField(max_length=2056, blank=True, default='')

    price = models.DecimalField(max_digits=16, decimal_places=2)
