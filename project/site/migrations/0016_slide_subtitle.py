# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-02 12:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site', '0015_auto_20181002_2151'),
    ]

    operations = [
        migrations.AddField(
            model_name='slide',
            name='subtitle',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
