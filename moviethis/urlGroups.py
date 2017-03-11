from django.conf.urls import url
from django.conf.urls.static import static

from Groups.views import *

urlGroups = [
    url(r'^groups/$', groups, name="groups"),
    url(r'^createGroup/$', createGroup, name="createGroup"),
    url(r'^group/(?P<id>[0-9]+)/?', group, name="group"),
    url(r'^addGroup/$', addGroup, name="addGroup"),
    url(r'^delegateGroup/$', delegateGroup, name="delegateGroup"),
    url(r'^deletePost/$', deletePost, name="deletePost"),
    url(r'^group/members/(?P<id>[0-9]+)/', groupMembers, name="groupMembers"),
    url(r'^deleteGroupUser/(?P<id>[0-9]+)/', deleteGroupUser, name="deleteGroupUser"),
    url(r'^deletePersonInterest/(?P<id>[0-9]+)/', deletePersonInterest, name="deletePersonInterest"),
    url(r'^addPersonInterest/(?P<id>[0-9]+)/', addPersonInterest, name="addPersonInterest"),
    url(r'^deleteMovieInterest/(?P<id>[0-9]+)/', deleteMovieInterest, name="deleteMovieInterest"),
    url(r'^addMovieInterest/(?P<id>[0-9]+)/', addMovieInterest, name="addMovieInterest"),
    url(r'^deleteGroup/(?P<id>[0-9]+)/', deleteGroup, name="deleteGroup"),
    url(r'^searchInterest/$', searchInterest, name="searchInterest"),
]
