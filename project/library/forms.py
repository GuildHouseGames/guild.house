# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from .models import Category, Game
from django import forms
from tinymce.widgets import TinyMCE
from . import models


class CategoryAdminForm(forms.ModelForm):

    class Meta(object):
        fields = ['title', 'heading', 'featured_content', 'content',
                  'meta_description', 'site', 'is_enabled']
        model = Category
        widgets = {'content': TinyMCE()}


class GameAdminForm(forms.ModelForm):

    class Meta(object):
        fields = ['title', 'heading', 'featured_content', 'content',
                  'meta_description', 'site', 'is_enabled']
        model = Game
        widgets = {'content': TinyMCE()}


# Maintenance Forms


class GameAddBGGForm(forms.Form):

    BGGID = forms.IntegerField(
        label='BGG ID',
        widget=forms.TextInput(attrs={'placeholder': 'eg. 31260'})
    )

    shelf = forms.ChoiceField(choices=models.CHOICE_LOCATIONS)

    priority = forms.ChoiceField(choices=models.CHOICE_PRIORITY)
