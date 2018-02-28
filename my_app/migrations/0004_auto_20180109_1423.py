# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-09 06:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0003_auto_20180109_1107'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plannedtask',
            fields=[
                ('plandkID', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=25)),
                ('conten', models.CharField(max_length=200)),
                ('staktype', models.CharField(max_length=10)),
                ('nowtime', models.CharField(max_length=6)),
                ('remndtime', models.DateTimeField()),
                ('settime', models.DateTimeField(auto_now_add=True)),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.User')),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='userid',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='my_app.User'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='clsslist',
            name='userid',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='my_app.User'),
            preserve_default=False,
        ),
    ]