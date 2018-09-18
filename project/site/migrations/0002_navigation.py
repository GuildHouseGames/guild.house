# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-17 06:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Navigation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('title', models.CharField(max_length=200)),
                ('url', models.CharField(max_length=200)),
                ('order', models.IntegerField(default=0)),
            ],
        ),
    ]
