# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import datetime, timedelta
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timesince import timesince
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField

from project import utils
from project.rolodex.models import Email, Phone
from . import querysets, settings


def get_current_site():
    try:
        return Site.objects.get_current().pk
    except Site.DoesNotExist:
        pass


class BookingDate(models.Model):

    date = models.DateField(db_index=True)

    total_num = models.PositiveIntegerField(default=0, null=True)

    total_pax = models.PositiveIntegerField(default=0, null=True)

    early_num = models.PositiveIntegerField(default=0, null=True)

    early_pax = models.PositiveIntegerField(default=0, null=True)

    lunch_num = models.PositiveIntegerField(default=0, null=True)

    lunch_pax = models.PositiveIntegerField(default=0, null=True)

    afternoon_num = models.PositiveIntegerField(default=0, null=True)

    afternoon_pax = models.PositiveIntegerField(default=0, null=True)

    main_num = models.PositiveIntegerField(default=0, null=True)

    main_pax = models.PositiveIntegerField(default=0, null=True)

    late_num = models.PositiveIntegerField(default=0, null=True)

    late_pax = models.PositiveIntegerField(default=0, null=True)

    objects = querysets.DateQuerySet.as_manager()

    class Meta:
        ordering = ['date']

    def set_values(self):
        date_bookings = Booking.objects.active().filter(
            reserved_date=self.date)
        pax = date_bookings.aggregate(models.Sum('party_size'))[
            'party_size__sum']
        num = date_bookings.count()
        if not getattr(self, 'total_pax') == pax:
            setattr(self, 'total_pax', pax)
            self.save()
        if not getattr(self, 'total_num') == num:
            setattr(self, 'total_num', num)
            self.save()

        for service, human in settings.SERVICE_CHOICE:
            date_service = date_bookings.filter(service=service)
            pax = date_service.aggregate(models.Sum('party_size'))[
                'party_size__sum']
            num = date_service.count()
            print(self.date, pax, num)

            if not getattr(self, '{}_pax'.format(service)) == pax:
                setattr(self, '{}_pax'.format(service), pax)
                self.save()
            if not getattr(self, '{}_num'.format(service)) == num:
                setattr(self, '{}_num'.format(service), num)
                self.save()

        return self

    def __str__(self):
        return "{} -- {} {} pax".format(self.date,
                                        self.total_num, self.total_pax)


@python_2_unicode_compatible
class Booking(models.Model):

    code = models.CharField(max_length=8, blank=True, default='')

    name = models.CharField(max_length=200)

    party_size = models.PositiveIntegerField(
        validators=[MaxValueValidator(100),
                    MinValueValidator(1)])

    status = models.CharField(max_length=50, choices=settings.STATUS_CHOICE,
                              default=settings.STATUS_CHOICE[0][0])

    is_cancelled = models.BooleanField(default=False)

    area = models.CharField(max_length=50, choices=settings.AREA_CHOICE,
                            default=settings.AREA_CHOICE[0][0])

    notes = models.TextField(blank=True, default='')

    private_notes = models.TextField(blank=True, default='')

    email = models.EmailField(max_length=150, blank=True, default='')

    phone = PhoneNumberField(
        help_text="One phone number only. Put additional numbers in 'notes' if necessary. We may need to confirm details so be sure to provide a good number."  # noqa
    )

    postcode = models.CharField(max_length=16, blank=True, default='')

    booking_method = models.CharField(
        max_length=50, choices=settings.METHOD_CHOICE,
        default=settings.METHOD_CHOICE[0][0],
        help_text="Only logged in people can see booking method."
    )

    site = models.ForeignKey('sites.Site', default=get_current_site,
                             related_name='bookings_booking',
                             on_delete=models.PROTECT)

    reserved_date = models.DateField(db_index=True)
    reserved_time = models.TimeField(db_index=True, default=timezone.now)

    booking_duration = models.DurationField(blank=True, null=True)

    service = models.CharField(max_length=50, choices=settings.SERVICE_CHOICE,
                               blank=True, default=''
                               )

    busy_night = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, editable=True)

    updated_at = models.DateTimeField(auto_now=True, editable=False)

    updated_by = models.ForeignKey(
        'auth.User', blank=True, null=True,
        related_name="booking_updated_by"
    )

    hear_choices = models.CharField(
        max_length=56, blank=True, default='',
        choices=settings.HEAR_CHOICE,
        verbose_name="Choices",
        help_text="How did you hear about us?"
    )

    hear_other = models.TextField(
        blank=True, default='',
        verbose_name="Other",
        help_text="Tell us a story about how you heard about us ..."  # noqa
    )

    legacy_code = models.CharField(max_length=256, blank=True, null=True)

    objects = querysets.QuerySet.as_manager()

    class Meta(object):
        ordering = ['reserved_date', 'reserved_time', 'name']
        verbose_name_plural = 'bookings'

    def __str__(self):
        desc = "{date} {start} {pax}pax {name}".format(
            name=self.name,
            pax=self.party_size,
            date=self.reserved_date.strftime("%d-%b-%Y"),
            start=self.reserved_time.strftime("%H:%M")
        )

        if self.booking_duration:
            desc = "{date} {start} {pax}pax {name}".format(
                name=self.name,
                pax=self.party_size,
                date=self.reserved_date.strftime("%d-%b-%Y"),
                start=self.reserved_time.strftime("%H:%M")
            )
        return desc

    def get_absolute_url(self):
        return reverse('bookings:booking_update', kwargs={'code': self.code})

    def get_next(self):
        queryset = self.__class__.objects.exclude(pk=self.pk).filter(
            site=self.site, reserved_date__gte=self.reserved_date
        ).active().order_by('reserved_date', 'reserved_time')
        return queryset.first()

    def get_previous(self):
        queryset = self.__class__.objects.exclude(pk=self.pk).filter(
            site=self.site, reserved_date__lte=self.reserved_date
        ).active().order_by('-reserved_date', 'reserved_time')
        return queryset.first()

    def is_active(self):
        return self in self.__class__.objects.filter(pk=self.pk).active()
    is_active.boolean = True
    is_active.short_description = 'active'

    def clean(self, *args, **kwargs):
        booking_date, is_created = BookingDate.objects.get_or_create(
            date=self.reserved_date)

        booking_list = Booking.objects.filter(reserved_date=self.reserved_date)

        # Check each 30min window to see which other bookings that window
        # conflicts with. If the total pax for that window exceeds the max
        # a validation error is thrown and the booking is not created.
        minutes = self.booking_duration.total_seconds() / 60
        # Potentially add an hour to match the safety hour often added
        blocks = int(minutes/30)
        for i in range(0, blocks):
            total_pax = 0
            dt_this = datetime.combine(
                self.reserved_date, self.reserved_time)
            dt_this = dt_this + timedelta(minutes=30*i)
            this_end = dt_this + timedelta(minutes=30)
            for booking in booking_list:
                dt_other = datetime.combine(
                    booking.reserved_date, booking.reserved_time)
                if (timesince(dt_other, dt_this).encode(
                        'ascii', 'ignore').decode('ascii') == '0minutes'):
                    # If not the same start (which shouldn't be skipped)
                    if not dt_this == dt_other:
                        # As it's just a half hour window if the window is
                        # before the other booking they can't overlap
                        continue
                # An hour is manually added on in views.TimeMixin for good
                # luck, so this needs to be accounted for
                booking_end = dt_other + \
                    booking.booking_duration + timedelta(minutes=60)
                # Essentially if the window starts after the booking starts
                # but ends before the booking ends
                if (timesince(booking_end, this_end).encode(
                        'ascii', 'ignore').decode('ascii') == '0minutes'):
                    total_pax = total_pax + booking.party_size
                    continue
            combined = self.party_size + total_pax

        super(Booking, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.clean()

        # Automatically make code if doesn't already have one.
        if not self.code:
            self.code = utils.generate_unique_hex(
                hex_field='code',
                queryset=Booking.objects.all())

            # adding on first creation. Messy, but works.
            # @@TODO make this less crap
            if "full" in self.private_notes:
                self.busy_night = True
                for booking in Booking.objects.filter(
                        reserved_date=self.reserved_date):
                    booking.busy_night = True
                    booking.save()

        # Automatically set `service` (eg. lunch) based upon `reserved_time`.
        for service_time, service in reversed(settings.SERVICE_TIMES):
            if self.reserved_time >= service_time:
                this_service = service
                break
        self.service = this_service

        if self.email:
            Email.objects.get_or_create(email=self.email)

        if self.phone:
            Phone.objects.get_or_create(phone=self.phone)

        if (self.status == 'no_show' and not self.is_cancelled) \
           or (self.status == 'cancelled' and not self.is_cancelled):
            self.is_cancelled = True

        if not (self.status == 'cancelled'
                or self.status == 'no_show') and self.is_cancelled:
            self.is_cancelled = False
        try:
            # Find the Booking and BookingDate objects relating to the
            # booking before modification
            previous_booking = Booking.objects.get(code=self.code)
            previous_booking_date = BookingDate.objects.get(
                date=previous_booking.reserved_date)

            # Save the new values for the booking
            super(Booking, self).save(*args, **kwargs)

            # Check if there are no Booking objects relating to the previous
            # BookingDate object
            bookings_on_previous_date = Booking.objects.filter(
                reserved_date=previous_booking.reserved_date)

            # Delete the previous BookingDate if there are no bookings
            if not bookings_on_previous_date:
                previous_booking_date.delete()
            # Update the previous BookingDate with the removed information
            else:
                previous_booking_date.set_values()
        # When creating a booking on a date with no bookings
        except (Booking.DoesNotExist, BookingDate.DoesNotExist):
            # Just save, create and update the BookingDate object with the
            # new Booking
            super(Booking, self).save(*args, **kwargs)
            booking_date, is_created = BookingDate.objects.get_or_create(
                date=self.reserved_date)
            booking_date.set_values()

    def delete(self):
        super(Booking, self).delete()
        booking_date, is_created = BookingDate.objects.get_or_create(
            date=self.reserved_date)
        bookings_on_date = Booking.objects.filter(
            reserved_date=self.reserved_date)
        if not bookings_on_date:
            booking_date.delete()
        else:
            booking_date.set_values()
