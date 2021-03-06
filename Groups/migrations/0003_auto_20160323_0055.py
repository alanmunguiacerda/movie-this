# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-23 06:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Groups', '0002_auto_20160320_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='movieInterest',
            field=models.ManyToManyField(blank=True, to='Movies.Movie'),
        ),
        migrations.AlterField(
            model_name='group',
            name='personInterest',
            field=models.ManyToManyField(blank=True, to='Persons.Person'),
        ),
    ]
