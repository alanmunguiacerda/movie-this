# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-24 02:54
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Nominations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='nomination',
            name='date',
            field=models.DateField(blank=True, default=datetime.datetime(2016, 3, 24, 2, 54, 23, 110311, tzinfo=utc)),
            preserve_default=False,
        ),
    ]