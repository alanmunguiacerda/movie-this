# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-23 06:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0002_remove_userprofile_ratedreviews'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='follows',
            field=models.ManyToManyField(blank=True, to='Users.UserProfile'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='groups', to='Groups.Group'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='groupsAdministrated',
            field=models.ManyToManyField(blank=True, related_name='groupsAdministrated', to='Groups.Group'),
        ),
    ]
