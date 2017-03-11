# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from Images.models import DefaultImage
from Users.models import UserProfile
from django.utils import timezone

# TODO: Incluir campo de género.

class Person(models.Model):
    birthDate = models.DateField()
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    pseudonym = models.CharField(max_length=100, blank=True)
    #gender = models.CharField()
    frontImage = models.ForeignKey('Images.PersonImage', blank=True, null=True, related_name="frontImage",  on_delete=models.SET_NULL)

    @property
    def age(self):
        now = timezone.now()
        return now.year - self.birthDate.year - ((now.month, now.day)<(self.birthDate.month,self.birthDate.day))

    @property
    def followers(self):
        followCount = UserProfile.objects.filter(favPersons = self).count()
        return followCount

    @property
    def fullName(self):
        return "{!s} {!s}".format(self.firstName, self.lastName)

    def __str__(self):
        if(self.pseudonym!=''):
            return ('{!s} \'{!s}\' {!s}').format(self.firstName, self.pseudonym, self.lastName)
        else:
            return ('{!s} {!s}').format(self.firstName, self.lastName)

    def getFrontImage(self):
        if not self.frontImage:
            return DefaultImage.objects.get(name="NoProfileImg").image.url
        else:
            return self.frontImage.image.url

class Rol(models.Model):
    rType = models.ForeignKey('Persons.RolType')
    rolRelation = models.ForeignKey("Persons.RolRelation")
    part = models.CharField(max_length=50, blank=True)
    screenTime = models.IntegerField(default=0)
    nominations = models.ManyToManyField('Nominations.Nomination', blank=True)

    def __str__(self):
        return ('{!s} as {!s} for {!s} minutes').format(self.rType, self.part, self.screenTime)

class RolType(models.Model):
    rType = models.CharField(max_length=50)
    def __str__(self):
        return self.rType

class RolRelation(models.Model):
    person = models.ForeignKey('Persons.Person', on_delete=models.CASCADE)
    movie = models.ForeignKey('Movies.Movie',  on_delete=models.CASCADE)

    def __str__(self):
        return ('{!s} participated in: {!s}').format(self.person, self.movie)

    class Meta:
        unique_together = (("person", "movie"),)
