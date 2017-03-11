from django.conf.urls import url
from django.conf.urls.static import static

from Users.views import *

urlUsers = [
    url(r'^$', home, name="index"),
    url(r'^logout/$', logout, name="logout"),
    url(r'^profile/$', profile, name="profile"),
    url(r'^my-groups/$', myGroups, name="myGroups"),
    url(r'^my-movies/$', myMovies, name="myMovies"),
    url(r'^my-persons/$', myPersons, name="myPersons"),
    url(r'^following/$', following, name="following"),
    url(r'^user/(?P<id>[0-9]*)$', user, name="user"),
    url(r'^followUser/$', followUser, name="followUser"),
]
