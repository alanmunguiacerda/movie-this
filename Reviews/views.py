import json

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from Reviews.models import *
from Users.models import *
from moviethis.commons.shortcuts import get_or_none


@login_required(login_url="/")
def rateReview(request):
	context = {}
	if request.method=="POST":
		idReview = request.POST.get('id', None)
		rate = request.POST.get('rate', None)
		review = get_or_none(Review, id=idReview)
		userProfile = get_or_none(UserProfile, user=request.user)
		if review != None and rate>=0 and userProfile!=None:
			rating = ReviewRate(review=review, user=userProfile, rate=rate)
			rating.save()
			context['newRate'] = ReviewRate.getReviewRateProm(review)
			context['rate'] = rate
			context['identif'] = context['identif'] = request.POST.get('identif', None)
	return HttpResponse(json.dumps(context), content_type='application/json')
