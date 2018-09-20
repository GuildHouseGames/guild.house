# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django import forms
from tinymce.widgets import TinyMCE
from phonenumber_field.formfields import PhoneNumberField
from .models import Booking
from .settings import (
    DURATION_SELECTION, BOOKING_TIMES_CHOICES, DEFAULT_BOOKING_DURATION)


class BookingAdminForm(forms.ModelForm):

    class Meta(object):
        fields = ['name', 'site', 'reserved_date', 'reserved_time']
        model = Booking


class BookingForm(forms.ModelForm):

    required_css_class = 'required'
    booking_duration = forms.ChoiceField(widget=forms.Select(),
                                         choices=DURATION_SELECTION)
    reserved_time = forms.ChoiceField(widget=forms.Select(),
                                      choices=BOOKING_TIMES_CHOICES)
    phone = PhoneNumberField(
        widget=forms.TextInput(attrs={'placeholder': '**'}))

    class Meta(object):
        fields = ['status', 'name', 'reserved_time', 'reserved_date',
                  'booking_duration', 'party_size', 'area', 'email', 'phone',
                  'postcode', 'notes', 'updated_by', 'booking_method',
                  'private_notes', 'busy_night']
        model = Booking
        widgets = {
            'notes': forms.Textarea(
                attrs={'rows': 4,  'width': 185, 'cols': 0}),
            'email': forms.TextInput(attrs={'placeholder': '**', }),
            'name': forms.TextInput(attrs={'placeholder': '**'}),
            'party_size': forms.TextInput(attrs={'placeholder': '**'}),
            'hear_other': forms.Textarea(
                attrs={'rows': 4,  'width': 185, 'cols': 0}),
        }

    def __init__(self, user=None, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields['phone'].required = True
        self.fields['email'].required = True
        self.fields['updated_by'].widget = forms.HiddenInput()

    def clean(self, *args, **kwargs):
        cleaned_data = super(BookingForm, self).clean(*args, **kwargs)
        if not cleaned_data.get('email') and not cleaned_data.get('phone'):
            raise forms.ValidationError(
                'Both a phone number and an email address are necessary for online bookings.')  # noqa
        if not cleaned_data.get('booking_duration'):
            cleaned_data['booking_duration'] = DEFAULT_BOOKING_DURATION
        return super(BookingForm, self).clean(*args, **kwargs)


class NewBookingForm(BookingForm):

    def __init__(self, user=None, *args, **kwargs):
        super(NewBookingForm, self).__init__(*args, **kwargs)
        self.fields['status'].widget = forms.HiddenInput()
        self.fields['private_notes'].widget = forms.HiddenInput()
        self.fields['busy_night'].widget = forms.HiddenInput()
        if not user.is_authenticated():
            self.fields['booking_method'].widget = forms.HiddenInput()


class BlankForm(forms.Form):

    input_data = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 15, 'cols': 100}))
