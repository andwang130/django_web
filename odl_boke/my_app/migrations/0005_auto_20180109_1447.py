# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-09 06:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0004_auto_20180109_1423'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plannedtask',
            old_name='nowtime',
            new_name='daytime',
        ),
        migrations.AddField(
            model_name='plannedtask',
            name='Interval',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]