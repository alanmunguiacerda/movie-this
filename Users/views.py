# -*- coding: utf-8 -*-
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

from models import *
from Groups.models import *
from Images.models import *
from Publications.models import *
from Movies.models import *
from Reviews.models import *

from moviethis.commons.shortcuts import get_or_none
# Create your views here.

def login(request, context):
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active == True:
            auth.login(request, user)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            context['errorToastMsg'].append('The user is deactivated')
            return render(request, 'index.html', context)
    else:
        context['errorToastMsg'].append('Incorrect user or password')

def register(request, context):
    username = request.POST.get('username', '')
    email = request.POST.get('email', '')
    firstname = request.POST.get('firstname', '')
    lastname = request.POST.get('lastname', '')
    password = request.POST.get('password', '')
    passwordR = request.POST.get('passwordR', '')
    if User.objects.filter(username=username).exists() == True:
        context['errorToastMsg'].append('That username is already taken')
    if User.objects.filter(email=email).exists() == True:
        context['errorToastMsg'].append('That email is already taken')
    if len(context['errorToastMsg']) > 0:
        pass
    else:
        newUser = User(username=username, email=email, first_name=firstname, last_name=lastname)
        newUser.set_password(password)
        newUser.save()
        tipoUsuario = get_or_none(UserType, nivel = 1)
        newUserProfile = UserProfile(user = newUser, userType=tipoUsuario)
        newUserProfile.save()

def home(request):
    context = {
        'pageName': 'Home',
        'pageUrl': '/',
        'errorToastMsg': [],
        'succesToastMsg':[],
    }
    if request.method == 'POST':
        type_req = request.POST.get('type','')
        if type_req == "login":
            login(request, context)
        elif type_req == "register":
            register(request, context)
    newMovies = Movie.objects.all().order_by('-id')[:8]
    mostLikedMovies = Movie.objects.annotate(likes=Count('userprofile')).order_by('-likes')[:4]
    bestMovieReviews = Review.objects.annotate(rated=Count('reviewrate')).order_by('-rated')[:8]
    context['newMovies'] = newMovies
    context['mostLikedMovies'] = mostLikedMovies
    context['bestMovieReviews'] = bestMovieReviews
    return render(request, 'index.html', context)

@login_required(login_url="/")
def logout(request):
    try:
        auth.logout(request)
    except KeyError:
        pass
    return redirect('index')

@login_required(login_url="/")
def updateProfileData(request, context):
    user = request.user
    email = request.POST.get('email','')
    first_name = request.POST.get('firstname','')
    last_name = request.POST.get('lastname','')
    query = User.objects.filter(email=email).exclude(username=user.username)
    if query.count() == 0:
        user.email=email
        user.first_name=first_name
        user.last_name=last_name
        user.save()
        context['succesToastMsg'].append('The profile information has been updated')
    else:
        context['errorToastMsg'].append('That email is already taken')

@login_required(login_url="/")
def changePasswordProfile(request, context):
    actPass = request.POST.get('actPass', '')
    newPass = request.POST.get('newPass', '')
    newPassR = request.POST.get('newPassR', '')
    user = request.user
    if user.check_password(actPass):
        if newPass == newPassR:
            user.set_password(newPass)
            user.save()
            user = authenticate(username=user.username, password=newPass)
            auth.login(request, user)
            context['succesToastMsg'].append('The password has been changed')
        else:
            context['errorToastMsg'].append('Passwords doesnt match')
    else:
        context['errorToastMsg'].append('Incorrect password')

@receiver(post_delete, sender=ProfileImage)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    try:
        if instance:
            if instance.file:
                if os.path.isfile(instance.file.path):
                    os.remove(instance.file.path)
    except:
        return False

@receiver(models.signals.pre_save, sender=ProfileImage)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_file = ProfileImage.objects.get(pk=instance.pk).image
    except ProfileImage.DoesNotExist:
        return False
    new_file = instance.image
    '''if old_file != new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)'''

@login_required(login_url="/")
def changeProfilePicture(request, context):
    userProfile = get_or_none(UserProfile, user = request.user)
    if userProfile != None:
        profImage = userProfile.profImage
        if profImage == None:
            newImg = ProfileImage(image = request.FILES['filePhoto'])
            newImg.save()
            userProfile.profImage = newImg
            userProfile.save()
        else:
            profImage = get_or_none(ProfileImage, pk = userProfile.profImage.pk)
            profImage.image = request.FILES['filePhoto']
            profImage.save()
    context['succesToastMsg'].append('Your profile picture has been updated')

@login_required(login_url="/")
def profile(request):
    context = {}
    context['errorToastMsg'] = []
    context['succesToastMsg'] = []
    userProfile = UserProfile.objects.get(user=request.user)
    if userProfile.profImage is None:
        profImage = DefaultImage.objects.get(name='NoProfileImg')
    else:
        profImage = ProfileImage.objects.get(pk = userProfile.profImage.pk )
    context['bigImage'] = profImage
    if request.method == "POST":
        type_req = request.POST.get('type','')
        if type_req == "updateDat":
            updateProfileData(request, context)
        elif type_req == "changePass":
            changePasswordProfile(request, context)
        elif type_req == "uploadPhoto":
            changeProfilePicture(request, context)
    return render(request,'profile.html', context)

@login_required(login_url="/")
def myGroups(request):
    context = {
        'pageName': 'My groups',
        'pageUrl': '/my-groups',
    }
    context['bigImage'] = DefaultImage.objects.get(name='logo')

    userProfile = get_or_none(UserProfile, user=request.user)
    group_list = userProfile.groups.all()
    paginator = Paginator(group_list, 20)

    page = request.GET.get('page')

    try:
    	context['groups'] = paginator.page(page)
    except PageNotAnInteger:
    	context['groups'] = paginator.page(1)
    except EmptyPage:
    	context['groups'] = paginator.page(paginator.num_pages)
    return render(request, 'groups.html', context)

@login_required(login_url="/")
def myMovies(request):
    context = {
        'pageName': 'Movies I like',
        'pageUrl': '/my-movies',
    }
    context['bigImage'] = DefaultImage.objects.get(name='logo')


    userProfile = get_or_none(UserProfile, user=request.user)
    movie_list = userProfile.favMovies.all()
    paginator = Paginator(movie_list, 12)

    page = request.GET.get('page')

    try:
    	context['movies'] = paginator.page(page)
    except PageNotAnInteger:
    	context['movies'] = paginator.page(1)
    except EmptyPage:
    	context['movies'] = paginator.page(paginator.num_pages)

    return render(request, 'movies.html', context)

@login_required(login_url="/")
def myPersons(request):
    context = {
        'pageName': 'People I like',
        'pageUrl': '/my-persons',
    }
    context['bigImage'] = DefaultImage.objects.get(name='logo')

    userProfile = get_or_none(UserProfile, user=request.user)
    persons_list = userProfile.favPersons.all()
    paginator = Paginator(persons_list, 12)

    page = request.GET.get('page')

    try:
    	context['persons'] = paginator.page(page)
    except PageNotAnInteger:
    	context['persons'] = paginator.page(1)
    except EmptyPage:
    	context['persons'] = paginator.page(paginator.num_pages)
    return render(request, 'persons.html', context)

@login_required(login_url="/")
def following(request):
    context = {
        'pageName': 'People I follow',
        'pageUrl': '/following',
    }
    context['bigImage'] = DefaultImage.objects.get(name='logo')

    userProfile = get_or_none(UserProfile, user=request.user)
    persons_list = userProfile.follows.all()
    paginator = Paginator(persons_list, 12)

    page = request.GET.get('page')

    try:
    	context['persons'] = paginator.page(page)
    except PageNotAnInteger:
    	context['persons'] = paginator.page(1)
    except EmptyPage:
    	context['persons'] = paginator.page(paginator.num_pages)
    return render(request, 'following.html', context)

@login_required(login_url="/")
def user(request, id):
    userProfile = get_or_none(UserProfile, user = id)
    context = {}
    context['userFound'] = userProfile
    if userProfile == None:
        context['errorToastMsg'] = []
        context['errorToastMsg'].append('User not found')
        return render(request, 'user.html', context)
    else:
        post = UserPost.objects.filter(user=userProfile)
        context['userFoundPost'] = post
        pub_list = UserPost.objects.filter(user=userProfile)
        paginator = Paginator(pub_list, 16)
        context['pubCount'] = pub_list.count()
        page = request.GET.get('page')

        try:
        	context['publications'] = paginator.page(page)
        except PageNotAnInteger:
        	context['publications'] = paginator.page(1)
        except EmptyPage:
        	context['publications'] = paginator.page(paginator.num_pages)
        return render(request, 'user.html', context)

def followUser(request):
    context = {}
    if request.method == 'POST':
        followId = request.POST.get('id', None)
        followUser = get_or_none(UserProfile, user  = followId)
        user = get_or_none(UserProfile, user = request.user )
        if followUser != None and user != None:
            if followUser in user.follows.all():
                context['remove'] = 1
                context['quitar'] = 'text-red-color'
                context['poner'] = 'text-primary-color'
                user.unfollowUser(followUser)
            else:
                context['poner'] = 'text-red-color'
                context['quitar'] = 'text-primary-color'
                context['remove'] = 0
                user.followUser(followUser)

            context['id'] = followId
            context['succesToastMsg'] = []

    return HttpResponse(json.dumps(context), content_type='application/json')
