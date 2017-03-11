from django.conf.urls import url
from django.conf.urls.static import static

from Reviews.views import *

urlReviews = [
    url(r'^rateReview/$', rateReview, name="rateReview"),
]
