# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-27 15:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_auto_20180428_1935'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='boardgamegeek_img',
            field=models.CharField(blank=True, default='', max_length=512),
        ),
    ]
