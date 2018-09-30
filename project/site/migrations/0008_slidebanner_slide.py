# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-25 23:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('site', '0007_slide_slidebanner'),
    ]

    operations = [
        migrations.AddField(
            model_name='slidebanner',
            name='slide',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='site.Slide'),
            preserve_default=False,
        ),
    ]