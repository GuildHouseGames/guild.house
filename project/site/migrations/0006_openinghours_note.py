# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-21 08:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site', '0005_auto_20180921_1732'),
    ]

    operations = [
        migrations.AddField(
            model_name='openinghours',
            name='note',
            field=models.CharField(blank=True, default='', max_length=256),
        ),
    ]
