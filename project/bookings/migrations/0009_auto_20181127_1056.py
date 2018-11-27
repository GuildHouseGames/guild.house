# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-26 23:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0008_auto_20181126_2126'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='deposit_amount_paid',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='is_paid_deposit',
            field=models.BooleanField(default=False),
        ),
    ]
