# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
import urllib, cStringIO
from PIL import Image
from django.db.models import Count, Min, Sum, Avg
from django.dispatch.dispatcher import receiver
from django.db.models.signals import pre_delete, post_delete

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from Users.models import UserProfile
from Images.models import DefaultImage, MovieImage
from moviethis.commons.shortcuts import get_or_none

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=150)
    desc = models.TextField(max_length=1000)
    releaseDate = models.DateField()
    categories = models.ManyToManyField('Movies.MovieCategory', blank=True)
    frontImage = models.ForeignKey('Images.MovieImage', blank=True, null=True, related_name="frontImage", on_delete=models.SET_NULL)

    @property
    def rate(self):
        ratesList = Rating.objects.filter(movie = self)
        if ratesList.count() > 0:
            rate = ratesList.aggregate(Avg('rate'))
            return rate['rate__avg']
        else:
            return "N/A"

    @property
    def followers(self):
        followCount = UserProfile.objects.filter(favMovies = self).count()
        print(followCount)
        return followCount

    def __str__(self):
        return ('{!s} ({!s})').format(self.title, self.releaseDate)

    def getFrontImage(self):
        if not self.frontImage:
            return DefaultImage.objects.get(name="defFrontImage").image.url
        else:
            return self.frontImage.image.url

    def setFrontImageURL(self, url):
        from django.core.files import File
        from urllib2 import urlopen
        from django.core.files.temp import NamedTemporaryFile

        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(urlopen(url).read())
        img_temp.flush()
        if self.frontImage == None:
            newImage = MovieImage(movie=self)
            name = "image_{!s}.jpg".format(self.pk)
            newImage.image.save(name, File(img_temp))
            newImage.save()
            self.frontImage = newImage
            self.save()

    @receiver(post_delete, sender=MovieImage)
    def auto_delete_file_on_delete(sender, instance, **kwargs):
        try:
            if instance:
                if instance.file:
                    if os.path.isfile(instance.file.path):
                        os.remove(instance.file.path)
        except:
            return False

    @receiver(models.signals.pre_save, sender=MovieImage)
    def auto_delete_file_on_change(sender, instance, **kwargs):
        if not instance.pk:
            return False
        try:
            old_file = MovieImage.objects.get(pk=instance.pk).image
        except MovieImage.DoesNotExist:
            return False
        new_file = instance.image
        if old_file != new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)

class MovieCategory(models.Model):
    category = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.category

class Rating(models.Model):
    movie = models.ForeignKey('Movies.Movie')
    user = models.ForeignKey('Users.UserProfile')
    rate = models.IntegerField(default=0,
            validators=[
                MaxValueValidator(10),
                MinValueValidator(0)
            ])
    def __str__(self):
        return ('{!s} rates {!s}: {!s}').format(self.user, self.movie, self.rate)

    def save(self, *args, **kwargs):
        ratingExist = get_or_none(Rating, movie = self.movie, user = self.user)
        if ratingExist == None:
            super(Rating, self).save(*args, **kwargs)
        else:
            ratingExist.rate = self.rate
            super(Rating, ratingExist).save(*args, **kwargs)

    @classmethod
    def getMovieRateProm(self, movie):
        ratesList = Rating.objects.filter(movie = movie)
        rate = ratesList.aggregate(Avg('rate'))
        return rate['rate__avg']
