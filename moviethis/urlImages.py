from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve

from Images.views import *

urlImages = [
	url(r'^site_media/(?P<path>.*)$', serve,
    {'document_root': settings.MEDIA_ROOT,
    'show_indexes' : True}),
]
