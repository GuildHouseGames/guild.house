# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-26 10:26
from __future__ import unicode_literals

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0007_auto_20181124_0932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_duration',
            field=models.DurationField(blank=True, default=datetime.timedelta(0, 14400), null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='party_size',
            field=models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)], verbose_name='Number of people'),
        ),
    ]
