# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-08 02:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vouchers', '0006_giftvoucher_is_legacy'),
    ]

    operations = [
        migrations.RenameField(
            model_name='giftvoucher',
            old_name='redemmed_date',
            new_name='redeemed_date',
        ),
    ]
