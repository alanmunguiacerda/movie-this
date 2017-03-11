# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Nomination(models.Model):
    winner = models.BooleanField(default=False)
    award = models.ForeignKey('Nominations.Award')
    date = models.DateField(blank=True, null=True);
    def __str__(self):
            return ('({!s}): {!s}').format(self.date, self.award)

    def isWinner(self):
        if self.winner:
            return 'yes'
        else:
            return 'no'

class Award(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
