# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-26 01:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Persons', '0003_person_frontimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='partMovies',
        ),
        migrations.AlterField(
            model_name='person',
            name='frontImage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='frontImage', to='Images.PersonImage'),
        ),
    ]
