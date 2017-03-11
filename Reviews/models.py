# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models import Count, Min, Sum, Avg
from django.core.validators import MaxValueValidator, MinValueValidator

from moviethis.commons.shortcuts import get_or_none

# Create your models here.

class Review(models.Model):
    user = models.ForeignKey('Users.UserProfile',  on_delete=models.CASCADE)
    movie = models.ForeignKey('Movies.Movie',  on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=3000)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return ('({!s}) {!s} reviwed {!s} : {!s}').format(self.date, self.user, self.movie, self.title)

    @property
    def rate(self):
        ratesList = ReviewRate.objects.filter(review = self)
        if ratesList.count() > 0:
            rate = ratesList.aggregate(Avg('rate'))
            return rate['rate__avg']
        else:
            return "N/A"

class ReviewRate(models.Model):
    user = models.ForeignKey('Users.UserProfile', on_delete=models.CASCADE)
    review = models.ForeignKey('Reviews.Review',  on_delete=models.CASCADE)
    rate = models.IntegerField(default=0,
            validators=[
                MaxValueValidator(10),
                MinValueValidator(0)
            ])
    def __str__(self):
        return ('{!s} rated a review : {!s}').format(self.user, self.rate)

    def save(self, *args, **kwargs):
        ratingExist = get_or_none(ReviewRate, review = self.review, user = self.user)
        if ratingExist == None:
            super(ReviewRate, self).save(*args, **kwargs)
        else:
            ratingExist.rate = self.rate
            super(ReviewRate, ratingExist).save(*args, **kwargs)

    @classmethod
    def getReviewRateProm(self, review):
        ratesList = ReviewRate.objects.filter(review = review)
        if ratesList.count() > 0:
            rate = ratesList.aggregate(Avg('rate'))
            return rate['rate__avg']
        else:
            return "N/A"

    @classmethod
    def getUserReviewRate(self, review, user):
        rate = get_or_none(ReviewRate, review=review, user=user)
        if rate != None:
            return rate.rate
        else:
            return 0
