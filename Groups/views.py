# -*- encoding: utf-8 -*-
import json

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from Groups.models import *
from Reviews.models import *
from Images.models import *
from Users.models import *
from Persons.models import Person
from Movies.models import Movie
from moviethis.commons.shortcuts import get_or_none

@login_required(login_url="/")
def createGroup(request):
	if request.method == 'POST':
		name = request.POST.get('name', '')
		if name.isEmptyString() == True:
			context['errorToastMsg'].append("A name is needed")
			return render(request, '/groups', context)
		owner = get_or_none(UserProfile, user=request.user)
		if owner == None:
			return redirect("groups")
	 	newGroup = Group.createGroup(name, owner)
		owner.addGroup(newGroup)
		owner.addGroupAdmin(newGroup)
	return redirect('groups')

@login_required(login_url="/")
def groups(request):
	context = {
        'pageName': 'Groups',
        'pageUrl': '/groups',
	}
	context['bigImage'] = DefaultImage.objects.get(name='logo')

	group_list = Group.objects.all()
	paginator = Paginator(group_list, 12)

	page = request.GET.get('page')

	try:
		context['groups'] = paginator.page(page)
	except PageNotAnInteger:
		context['groups'] = paginator.page(1)
	except EmptyPage:
		context['groups'] = paginator.page(paginator.num_pages)
	return render(request, 'groups.html', context)

@login_required(login_url="/")
def changeGroupPicture(request, context):
	group = get_or_none(Group, pk = context['group'].pk)
	if group != None:
	    frontImage = group.frontImage
	    if frontImage == None:
	        newImg = GroupImage(image = request.FILES['filePhoto'])
	        newImg.save()
	        group.frontImage = newImg
        	group.save()
	    else:
			frontImage = get_or_none(GroupImage, pk= context['group'].frontImage.pk)
			frontImage.image = request.FILES['filePhoto']
			frontImage.save()
	return redirect('group', id=group.pk)

@login_required(login_url="/")
def group(request, id):
	context = {}
	post_list = Post.objects.filter(group__id = id).order_by('date').reverse()
	paginator = Paginator(post_list, 12)
	userCount = UserProfile.objects.filter( groups__pk = id ).count()
	group = get_or_none(Group, id = id)

	context['group'] = Group.objects.get(pk = id)
	context['page'] = request.GET.get('page')
	context['bigImage'] = DefaultImage.objects.get(name='logo')
	context['pageName'] = context['group'].name
	context['pageUrl'] = '/group/{!s}'.format(context['group'].id)
	context['userCount'] = userCount
	context['errorToastMsg'] = []
	try:
		context['post'] = paginator.page(context['page'])
	except PageNotAnInteger:
		context['post'] = paginator.page(1)
	except EmptyPage:
		context['post'] = paginator.page(paginator.num_pages)

	if request.method == "POST":
		if request.POST.get('type', '') == 'sendPost':
			content = request.POST.get('content', '')
			if not group in get_or_none(UserProfile, user=request.user).groups.all():
				context['errorToastMsg'].append('Join to comment')
				return render(request, 'group.html', context)
			if content.isspace() or content == None:
				context['errorToastMsg'].append('You must write something to publish')
				return render(request, 'group.html', context)
			else:
				user = UserProfile.objects.get(user=request.user)
				newPost = Post(user=user, group=context['group'], content=content)
				newPost.save()
				return redirect('group', id='{!s}'.format(id))
		elif request.POST.get('type', '') == 'change':
			username = request.POST.get('newOwner', '')
			user = get_or_none(User, username = username)
			newOwner = get_or_none(UserProfile, user = user)
			if group.owner.user == request.user:
				if newOwner:
					group.setOwner(newOwner)
					return redirect('group', id=id)
				else:
					context['errorToastMsg'].append('User not found')
			else:
				context['errorToastMsg'].append('You are not the owner of this group')
		elif request.POST.get('type', '') == 'leave':
			user = get_or_none(UserProfile, user = request.user)
			if group.owner == user:
				context['errorToastMsg'].append('Assign a new owner first')
			else:
				user.groups.remove(group)
				user.groupsAdministrated.remove(group)
				return redirect('group', id=id)
		elif request.POST.get('type', '') == 'uploadPhoto':
			return changeGroupPicture(request, context)
	return render(request,  'group.html', context )

@login_required(login_url="/")
def addGroup(request):
	context = {}
	if request.method == 'POST':
		userProfile = UserProfile.objects.get(user=request.user)
		groupId = request.POST.get('groupId', None)
		group = get_object_or_404(Group, id = groupId)
		if group in userProfile.groups.all():
			context['quitar'] = 'text-red-color'
			context['poner'] = 'text-primary-color'
			context['remove'] = '1'
			if userProfile.removeGroup(group) == False:
				context['errorToastMsg'] = 'Assign a new owner first'
				context['remove'] = '2'
		else:
			context['poner'] = 'text-red-color'
			context['quitar'] = 'text-primary-color'
			context['remove'] = '0'
			print("En func")
			userProfile.addGroup(group)
			print("En func")
		context['id'] = '{!s}'.format(groupId)
		context['groupName'] = group.name
	return HttpResponse(json.dumps(context), content_type='application/json')

@login_required(login_url="/")
def delegateGroup(request):
	pass

@login_required(login_url="/")
def deletePost(request):
	context = {}
	if request.method == 'POST':
		userProfile = UserProfile.objects.get(user=request.user)
		postId = request.POST.get('id', None)
		post = get_or_none(Post, id=postId)
		if post.user == userProfile or post.group.owner == userProfile:
			post.delete()
			context['succesToastMsg'] = 'Comment deleted'
			context['id'] = '{!s}'.format(postId)
	return HttpResponse(json.dumps(context), content_type='application/json')

@login_required(login_url="/")
def groupMembers(request, id):
	members = UserProfile.objects.filter( groups__pk = id )
	group = get_or_none(Group, id=id)
	context = {
		'pageName': "{!s}".format(group.name),
		'pageUrl': "/group/{!s}/".format(group.id),
		'group' : group,
		'members' : members,
	}
	return render(request, 'groupMembers.html', context)

@login_required(login_url="/")
def deleteGroup(request, id):
	userProfile = UserProfile.objects.get(user=request.user)
	group = get_or_none(Group, id=id)
	if(userProfile !=None and group != None):
		if(userProfile == group.owner):
			group.deleteGroup()
	context={}
	context['redirect'] = "/groups/"
	return HttpResponse(json.dumps(context), content_type='application/json')

@login_required(login_url="/")
def deleteGroupUser(request, id):
	context = {}
	if request.method == 'POST':
		userProfile = UserProfile.objects.get(user=request.user)
		group = get_or_none(Group, id=id)
		if request.user == group.owner.user:
			userDeleteId = request.POST.get('id',None)
			userDelete = get_or_none(UserProfile, user__id=userDeleteId)
			if userDelete == group.owner:
				context['errorToastMsg'] = 'Assign a new owner first'
			else:
				userDelete.removeGroup(group)
				context['id'] = '{!s}'.format(userDeleteId)
	return HttpResponse(json.dumps(context), content_type='application/json')

@login_required(login_url="/")
def addPersonInterest(request, id):
	context = {}
	if request.method == 'POST':
		userProfile = UserProfile.objects.get(user=request.user)
		group = get_or_none(Group, id=id)
		if request.user == group.owner.user:
			interestAdded = request.POST.get('id',None)
			personAdded = get_or_none(Person, id=interestAdded)
			group.addPerson(personAdded)
			context['id'] = '{!s}'.format(interestAdded)
			context['succesToastMsg'] = "{!s} added to interests".format(personAdded.fullName)
	return HttpResponse(json.dumps(context), content_type='application/json')

@login_required(login_url="/")
def deletePersonInterest(request, id):
	context = {}
	if request.method == 'POST':
		userProfile = UserProfile.objects.get(user=request.user)
		group = get_or_none(Group, id=id)
		if request.user == group.owner.user:
			interestDeleted = request.POST.get('id',None)
			personDelete = get_or_none(Person, id=interestDeleted)
			group.removePerson(personDelete)
			context['id'] = '{!s}'.format(interestDeleted)
	return HttpResponse(json.dumps(context), content_type='application/json')

@login_required(login_url="/")
def addMovieInterest(request, id):
	context = {}
	if request.method == 'POST':
		userProfile = UserProfile.objects.get(user=request.user)
		group = get_or_none(Group, id=id)
		if request.user == group.owner.user:
			interestAdded = request.POST.get('id',None)
			movieAdded = get_or_none(Movie, id=interestAdded)
			group.addMovie(movieAdded)
			context['id'] = '{!s}'.format(interestAdded)
			context['succesToastMsg'] = "{!s} added to interests".format(movieAdded.title)
	return HttpResponse(json.dumps(context), content_type='application/json')

@login_required(login_url="/")
def deleteMovieInterest(request, id):
	context = {}
	if request.method == 'POST':
		userProfile = UserProfile.objects.get(user=request.user)
		group = get_or_none(Group, id=id)
		if request.user == group.owner.user:
			interestDeleted = request.POST.get('id',None)
			movieDelete = get_or_none(Movie, id=interestDeleted)
			group.removeMovie(movieDelete)
			context['id'] = '{!s}'.format(interestDeleted)
	return HttpResponse(json.dumps(context), content_type='application/json')

@login_required(login_url="/")
def searchInterest(request):
	context = {}
	if request.method == 'POST':
		search = request.POST.get('search', None)
		search = '%{!s}%'.format(search)
		if len(search) > 2:
			movieInterestFound = Movie.objects.extra(where=["title like '"+search+"'"]).values_list('id', 'title')
			personInterestFound = Person.objects.extra(where=["firstName like '"+search+"'"] ).values_list('id', 'firstName', 'lastName')
			context['movieInterestFound'] = list(movieInterestFound)
			context['personInterestFound'] = list(personInterestFound)
	return HttpResponse(json.dumps(context), content_type='application/json')
