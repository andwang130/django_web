# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-19 10:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0013_projectplan_urlgithub'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectfile',
            name='filename',
            field=models.CharField('sdsds', max_length=25),
            preserve_default=False,
        ),
    ]