# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from .models import MenuType
from django import forms
from tinymce.widgets import TinyMCE


# class MenuAdminForm(forms.ModelForm):

#     class Meta(object):
#         fields = ['title', 'heading', 'summary', 'menu_file',
#                   'is_enabled', 'is_featured', 'site', 'publish_at']
#         model = Menu
#         widgets = {'content': TinyMCE()}


class MenuTypeAdminForm(forms.ModelForm):

    class Meta(object):
        fields = [
            'is_enabled', 'type', 'order',  'title', 'summary',
            'publish_at', 'menu_file'
        ]
        model = MenuType
        widgets = {'summary': TinyMCE()}
