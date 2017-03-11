from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.template.defaulttags import register

from Users.models import *
from Images.models import *

def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None

def navContext(request):
    data = {
    'noProfileImg': get_or_none(DefaultImage, name='NoProfileImg'),
    'logoImg': get_or_none(DefaultImage, name='logo'),
    'groupImg': get_or_none(DefaultImage, name='group'),
    'bigImg': get_or_none(DefaultImage, name='logo'),
    }
    if request.user.is_authenticated() == True:
        userProfile = UserProfile.objects.get(user=request.user)
        data['user'] = request.user
        data['userProfile'] = userProfile
    return data

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
