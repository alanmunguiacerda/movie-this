# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth import authenticate

from django.contrib.auth.models import User
from Images.models import DefaultImage

class UserType(models.Model):
    rol = models.CharField(max_length=20)
    nivel = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.rol

class UserProfile(models.Model):
    user = models.OneToOneField(User,  primary_key=True)
    userType = models.ForeignKey('Users.UserType')
    follows = models.ManyToManyField('Users.UserProfile', blank=True)
    groups = models.ManyToManyField('Groups.Group', related_name="groups", blank=True)
    groupsAdministrated = models.ManyToManyField('Groups.Group', related_name="groupsAdministrated", blank=True)
    favMovies = models.ManyToManyField('Movies.Movie', blank=True)
    favPersons = models.ManyToManyField('Persons.Person', blank=True)
    profImage = models.ForeignKey('Images.ProfileImage', blank=True, null=True,  on_delete=models.SET_NULL)

    def __str__(self):
        return self.user.username

    def addGroup(self, group):
        self.groups.add(group)

    def addGroupAdmin(self, group):
        self.groupsAdministrated.add(group)

    def removeGroup(self, group):
        if group.owner != self:
            self.groups.remove(group)
            self.groupsAdministrated.remove(group)
            return True
        return False

    def removeGroupAdmin(self, group):
        if group.owner != self:
            self.groupsAdministrated.remove(group)
            return True
        return False

    def addMovie(self, movie):
        self.favMovies.add(movie)

    def removeMovie(self, movie):
        self.favMovies.remove(movie)

    def addPerson(self, person):
        self.favPersons.add(person)

    def removePerson(self, person):
        self.favPersons.remove(person)

    def followUser(self, user):
        self.follows.add(user)

    def unfollowUser(self, user):
        self.follows.remove(user)

    def getProfilePicture(self):
        if not self.profImage:
            return DefaultImage.objects.get(name="NoProfileImg").image.url
        else:
            return self.profImage.image.url
