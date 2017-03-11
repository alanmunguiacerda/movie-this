from django.conf.urls import url
from django.conf.urls.static import static

from Publications.views import *

urlPublications = [
    url(r'^post/$', publications, name='publications'),
    url(r'^newUserPost/$', newUserPost, name='newUserPost'),
    url(r'^deleteUserPost/$', deleteUserPost, name='deleteUserPost'),
]
