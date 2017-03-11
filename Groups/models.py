# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from Images.models import DefaultImage

# Create your models here.

class Group(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey('Users.UserProfile', null=True, on_delete=models.SET_NULL)
    creationDate = models.DateField(auto_now_add=True)
    personInterest = models.ManyToManyField('Persons.Person', blank=True)
    movieInterest = models.ManyToManyField('Movies.Movie', blank=True)
    frontImage = models.ForeignKey('Images.GroupImage', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    def setOwner(self, userProfile):
        userProfile.groups.add(self)
        userProfile.groupsAdministrated.add(self)
        self.owner=userProfile
        self.save()

    @classmethod
    def createGroup(cls, name, userProfile):
        group = cls(name=name, owner=userProfile)
        group.save()
        return group

    def deleteGroup(cls):
        deleted = cls.delete()
        return deleted

    def getProfilePicture(self):
        if not self.frontImage:
            return DefaultImage.objects.get(name="group").image.url
        else:
            return self.frontImage.image.url

    def removePerson(self, person):
        self.personInterest.remove(person)

    def addPerson(self, person):
        self.personInterest.add(person)

    def removeMovie(self, movie):
        self.movieInterest.remove(movie)

    def addMovie(self, movie):
        self.movieInterest.add(movie)

class Post(models.Model):
    user = models.ForeignKey('Users.UserProfile')
    group = models.ForeignKey('Groups.Group', null=True, on_delete=models.SET_NULL)
    content = models.CharField(max_length=500)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return ('({!s}) {!s}: {!s}').format(self.date, self.user.user.username, self.content)
