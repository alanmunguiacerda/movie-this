# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-24 02:54
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Groups', '0003_auto_20160323_0055'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='date',
            field=models.DateField(auto_now_add=True, default=datetime.datetime(2016, 3, 24, 2, 54, 13, 814558, tzinfo=utc)),
            preserve_default=False,
        ),
    ]