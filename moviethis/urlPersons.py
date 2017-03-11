from django.conf.urls import url
from django.conf.urls.static import static

from Persons.views import *

urlPersons = [
    url(r'^people/$', people, name="people"),
    url(r'^person/(?P<id>[0-9]+)', person, name="person"),
    url(r'^likePerson/$', likePerson, name="likePerson"),
]
