# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-29 23:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cq', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='ts',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now),
        ),
    ]
