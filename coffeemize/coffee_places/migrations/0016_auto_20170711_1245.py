# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-11 12:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coffee_places', '0015_auto_20170711_1149'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coffeeplace',
            name='avatar_url',
        ),
        migrations.RemoveField(
            model_name='coffeeplace',
            name='image_url',
        ),
        migrations.AddField(
            model_name='coffeeplace',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='coffee_places/avatars'),
        ),
    ]
