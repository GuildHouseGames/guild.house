# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from . import querysets, settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from project import utils
from taggit.managers import TaggableManager


def get_current_site():
    try:
        return Site.objects.get_current().pk
    except Site.DoesNotExist:
        pass


@python_2_unicode_compatible
class Entry(models.Model):

    title = models.CharField(max_length=200, blank=True, default='')

    heading = models.CharField(max_length=200, blank=True, default='')

    summary = models.TextField(blank=True, default='')

    featured_image = models.ImageField(
        max_length=1024,
        upload_to='entry_featured',
        help_text='Ensure bigger than 790x377 if going to be featured in carousel.',  # noqa
        blank=True, default=''
    )

    featured_order = models.IntegerField(default=0)

    featured_content = models.TextField(blank=True, default='')

    content = models.TextField(blank=True, default='')

    summary = models.TextField(blank=True, default='')

    tags = TaggableManager(blank=True)

    meta_description = models.CharField(max_length=200, blank=True, default='')

    is_enabled = models.BooleanField('enabled', db_index=True, default=True)

    is_featured = models.BooleanField('featured', db_index=True, default=False)

    site = models.ForeignKey(
        'sites.Site', default=get_current_site,
        related_name='blog_entries',
        on_delete=models.PROTECT
    )

    slug = models.SlugField(unique_for_date='publish_at')

    publish_at = models.DateTimeField(db_index=True, default=timezone.now)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    updated_at = models.DateTimeField(auto_now=True, editable=False)

    objects = querysets.QuerySet.as_manager()

    class Meta(object):
        ordering = ['featured_order', '-publish_at', 'title']
        unique_together = ['site', 'publish_at', 'slug']
        verbose_name_plural = 'entries'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        server_timezone = timezone.pytz.timezone(settings.TIME_ZONE)

        if timezone.is_naive(self.publish_at):
            publish_at = server_timezone.localize(self.publish_at)
        else:
            publish_at = server_timezone.normalize(self.publish_at)

        return reverse('blog:entry_detail',
                       kwargs={'year': '%04d' % (publish_at.year),
                               'month': '%02d' % (publish_at.month),
                               'slug': self.slug})

    def get_next(self):
        queryset = self.__class__.objects.exclude(pk=self.pk).filter(
            site=self.site, publish_at__gte=self.publish_at
        ).active().order_by('publish_at')
        return queryset.first()

    def get_previous(self):
        queryset = self.__class__.objects.exclude(pk=self.pk).filter(
            site=self.site, publish_at__lte=self.publish_at
        ).active().order_by('-publish_at')
        return queryset.first()

    def is_active(self):
        return self in self.__class__.objects.filter(pk=self.pk).active()
    is_active.boolean = True
    is_active.short_description = 'active'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = utils.generate_unique_slug(
                self.title,
                self.__class__.objects.filter(
                    site=self.site,
                    publish_at__year=self.publish_at.year,
                    publish_at__month=self.publish_at.month,
                    publish_at__day=self.publish_at.day))
        return super(Entry, self).save(*args, **kwargs)
