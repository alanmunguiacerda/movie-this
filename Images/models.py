# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import os
from PIL import Image

from django.db import models

class MovieImage(models.Model):
	image = models.ImageField(upload_to = 'movies/')
	movie = models.ForeignKey('Movies.Movie', null=True, on_delete=models.SET_NULL)
	def __str__(self):
		return os.path.basename(self.image.name)

	def save(self, width=800, height=1200):
		if self.image == None:
			return
		super(MovieImage, self).save()
		imageO = Image.open(self.image)
		size = ( width, height)
		imageO = imageO.resize(size, Image.ANTIALIAS)
		imageO.save(self.image.path)

class ProfileImage(models.Model):
	image = models.ImageField(upload_to = 'profile/')
	def __str__(self):
		return  os.path.basename(self.image.name)

	def save(self, width=500, height=500):
		if self.image == None:
			return
		super(ProfileImage, self).save()
		imageO = Image.open(self.image)
		size = ( width, height)
		imageO = imageO.resize(size, Image.ANTIALIAS)
		imageO.save(self.image.path)

class DefaultImage(models.Model):
	name = models.CharField(max_length=50, unique=True)
	image = models.ImageField(upload_to = 'default/')
	def __str__(self):
		return  os.path.basename(self.image.name)

class GroupImage(models.Model):
	image = models.ImageField(upload_to = 'groups/')
	def __str__(self):
		return os.path.basename(self.image.name)

	def save(self, width=800, height=800):
		if self.image == None:
			return
		super(GroupImage, self).save()
		imageO = Image.open(self.image)
		size = ( width, height)
		imageO = imageO.resize(size, Image.ANTIALIAS)
		imageO.save(self.image.path)

class PersonImage(models.Model):
	image = models.ImageField(upload_to = 'persons/')
	person = models.ForeignKey('Persons.Person')
	def __str__(self):
		return os.path.basename(self.image.name)

	def save(self, width=800, height=1200):
		if self.image == None:
			return
		super(PersonImage, self).save()
		imageO = Image.open(self.image)
		size = ( width, height)
		imageO = imageO.resize(size, Image.ANTIALIAS)
		imageO.save(self.image.path)
