# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-25 09:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Movies', '0004_movie_frontimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='desc',
            field=models.TextField(default='Prueba', max_length=1000),
            preserve_default=False,
        ),
    ]