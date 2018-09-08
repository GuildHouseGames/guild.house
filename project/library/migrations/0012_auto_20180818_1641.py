# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-18 06:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0011_auto_20180816_1819'),
    ]

    operations = [
        migrations.CreateModel(
            name='CopyHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person', models.CharField(blank=True, default='', max_length=64, null=True)),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
                ('is_play', models.BooleanField(default=False)),
                ('notes', models.TextField(blank=True, default='')),
                ('state', models.CharField(blank=True, choices=[('unknown', 'unknown'), ('great', 'Great'), ('fine', 'Fine'), ('poor', 'Poor'), ('refill', 'Replenish consumables'), ('empty', 'Completely out of consumables'), ('missing', 'Parts missing'), ('fixable', 'Broken, maybe fixable'), ('broken', 'Broken, might be dead'), ('unplayable', "It's dead, Jim")], default='', max_length=256, null=True)),
            ],
        ),
        migrations.RenameModel(
            old_name='GameInLibrary',
            new_name='Copy',
        ),
        migrations.AlterModelOptions(
            name='series',
            options={'ordering': ['name'], 'verbose_name_plural': 'series'},
        ),
        migrations.RenameField(
            model_name='copy',
            old_name='is_broken',
            new_name='is_dead',
        ),
        migrations.AddField(
            model_name='copyhistory',
            name='copy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='library.Copy'),
        ),
    ]
