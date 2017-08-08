# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-07 18:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CoffeePlace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=256, null=True)),
                ('url', models.URLField(blank=True)),
                ('phone', models.CharField(blank=True, max_length=15)),
                ('address', models.CharField(blank=True, max_length=256)),
                ('hours', models.CharField(blank=True, max_length=256)),
                ('price', models.CharField(blank=True, max_length=256)),
                ('rating', models.DecimalField(decimal_places=1, max_digits=2)),
                ('tips', models.TextField(blank=True)),
                ('tips_url', models.URLField(blank=True)),
                ('image', models.ImageField(upload_to='coffee_places')),
                ('category', models.CharField(blank=True, max_length=256, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]