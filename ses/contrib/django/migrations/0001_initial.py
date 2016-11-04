# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-22 16:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ts', models.DateTimeField(default=django.utils.timezone.now)),
                ('entity_id', models.CharField(db_index=True, max_length=128)),
                ('name', models.CharField(db_index=True, max_length=128)),
                ('data', jsonfield.fields.JSONField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UniqueItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('namespace', models.CharField(max_length=128)),
                ('value', models.CharField(max_length=255)),
                ('entity_id', models.CharField(max_length=128)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='uniqueitem',
            unique_together=set([('namespace', 'value')]),
        ),
    ]