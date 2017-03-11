import json

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.signals import pre_delete, post_delete
from django.dispatch.dispatcher import receiver
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from Publications.models import *
from Images.models import *
from Users.models import UserProfile

from moviethis.commons.shortcuts import get_or_none

@login_required(login_url="/")
def publications(request):
		context = {
	        'pageName': 'Post',
	        'pageUrl': '/post',
		}
		context['bigImage'] = DefaultImage.objects.get(name='logo')

		pub_list = UserPost.objects.filter(user__user=request.user)
		paginator = Paginator(pub_list, 16)
		context['pubCount'] = pub_list.count()
		page = request.GET.get('page')

		try:
			context['publications'] = paginator.page(page)
		except PageNotAnInteger:
			context['publications'] = paginator.page(1)
		except EmptyPage:
			context['publications'] = paginator.page(paginator.num_pages)

		return render(request, 'post.html', context)


@login_required(login_url="/")
def newUserPost(request):
	if request.method == "POST":
		content = request.POST.get('content', None)
		user = get_or_none(UserProfile, user = request.user)
		if content != None and user != None:
			newPost = UserPost(user=user, content=content)
			newPost.save()
	return redirect('publications')

@login_required(login_url="/")
def deleteUserPost(request):
	context = {}
	if request.method == 'POST':
		userProfile = UserProfile.objects.get(user=request.user)
		postId = request.POST.get('id', None)
		post = get_or_none(UserPost, id=postId)
		if post.user == userProfile:
			post.delete()
			context['succesToastMsg'] = 'Post deleted'
			context['id'] = '{!s}'.format(postId)
		return HttpResponse(json.dumps(context), content_type='application/json')
