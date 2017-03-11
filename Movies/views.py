# -*- encoding: utf-8 -*-
import json
from datetime import date
import re

from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from Movies.models import *
from Reviews.models import *
from Images.models import *
from Users.models import *
from moviethis.commons.shortcuts import get_or_none

# TODO: rate system.

def movies(request):
	context = {
        'pageName': 'Movies',
        'pageUrl': '/movies',
	}
	context['bigImage'] = DefaultImage.objects.get(name='logo')

	movie_list = Movie.objects.all()
	paginator = Paginator(movie_list, 16)
	context['movieCount'] = movie_list.count()
	page = request.GET.get('page')

	try:
		context['movies'] = paginator.page(page)
	except PageNotAnInteger:
		context['movies'] = paginator.page(1)
	except EmptyPage:
		context['movies'] = paginator.page(paginator.num_pages)

	return render(request, 'movies.html', context)

def movie(request, id):
	context = {}
	review_list = Review.objects.filter(movie__pk = id)
	paginator = Paginator(review_list, 12)

	context['movie'] = Movie.objects.get(pk = id)
	context['page'] = request.GET.get('page')
	context['bigImage'] = DefaultImage.objects.get(name='logo')
	context['pageName'] = context['movie'].title
	context['pageUrl'] = '/movie/{!s}'.format(context['movie'].id)

	if(request.user.is_authenticated()):
		userProfile = get_or_none(UserProfile, user=request.user)
		if(userProfile!=None):
			context['userRate'] = get_or_none(Rating, movie=context['movie'], user=userProfile)

	try:
		context['reviews'] = paginator.page(context['page'])
	except PageNotAnInteger:
		context['reviews'] = paginator.page(1)
	except EmptyPage:
		context['reviews'] = paginator.page(paginator.num_pages)
	return render(request, 'movie.html', context )

@login_required(login_url="/")
def reviewMovie(request, id):
	if request.method == "POST":
		title = request.POST.get('title', None)
		content = request.POST.get('content', None)
		movie = get_or_none(Movie, id=id)
		user = get_or_none(UserProfile, user=request.user)
		if movie and user:
			newReview = Review(title=title, content=content, movie=movie, user=user)
			newReview.save()
		return redirect('/movie/{!s}'.format(id))

@login_required(login_url="/")
def likeMovie(request):
	context = {}

	if request.method == 'POST':
		userProfile = UserProfile.objects.get(user=request.user)
		movieId = request.POST.get('movieId', None)
		movie = get_or_none(Movie, id = movieId)

		if movie in userProfile.favMovies.all():
			context['quitar'] = 'text-red-color'
			context['poner'] = 'text-primary-color'
			context['remove'] = '1'
			userProfile.removeMovie(movie)
		else:
			context['poner'] = 'text-red-color'
			context['quitar'] = 'text-primary-color'
			context['remove'] = '0'
			userProfile.addMovie(movie)
		context['id'] = '{!s}'.format(movieId)
		context['movieTitle'] = movie.title
		context['movieYear'] = movie.releaseDate.year
		context['favCount'] = movie.followers
	return HttpResponse(json.dumps(context), content_type='application/json')

@login_required(login_url="/")
def deleteReview(request):
	context={}
	if request.method == "POST":
		id = request.POST.get("id", None)
		review = get_or_none(Review, id=id)
		if review and review.user.user == request.user:
			review.delete()
			context['id'] = id
			context['succesToastMsg'] = "Review deleted"
	return HttpResponse(json.dumps(context), content_type='application/json')

@login_required(login_url="/")
def loadMovies(request):
	if request.method == "POST":
		doc = request.FILES['csvFile']
		catAll = MovieCategory.objects.all()
		if doc != None:
			lines = doc.readlines()
			for f in lines:
				datos = re.split('\', \'|\',\'', f, 3)
				title = datos[0].translate(None, '\'')
				desc = datos[1]
				dateV = date(day=1, month=1, year=int(datos[2]))
				nueva = Movie(title=title, desc=desc, releaseDate=dateV)
				catList = datos[3].translate(None, '\'')
				catList = catList.translate(None, '\n')
				catList = catList.translate(None, '\r')
				catList = catList.split(',')
				nueva.save()
				cats = []
				for c in catList:
					cat, created = MovieCategory.objects.get_or_create(category = c)
					cats.append(cat)
				nueva.categories.add(*cats)
	return redirect('movies')

@login_required(login_url="/")
def assignImage(request, id):
	if request.method=='POST':
		movie = get_or_none(Movie, id=id)
		url = request.POST.get('url', None)
		if movie != None:
			movie.setFrontImageURL(url)
	return redirect('movie', id=id)

@login_required(login_url="/")
def rateMovie(request):
	context = {}
	if request.method=="POST":
		idMovie = request.POST.get('id', None)
		rate = request.POST.get('rate', None)
		movie = get_or_none(Movie, id=idMovie)
		userProfile = get_or_none(UserProfile, user=request.user)
		if movie != None and rate>=0 and userProfile!=None:
			rating = Rating(movie=movie, user=userProfile, rate=rate)
			print rating
			rating.save()
			context['newRate'] = Rating.getMovieRateProm(movie)
			context['rate'] = rate
			context['identif'] = request.POST.get('identif', None)
	return HttpResponse(json.dumps(context), content_type='application/json')
