# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-09 19:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coffee_places', '0002_auto_20170309_1524'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coffeeplace',
            name='user',
        ),
    ]
