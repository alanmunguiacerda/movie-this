from django.conf.urls import url
from django.conf.urls.static import static

from Movies.views import *

urlMovies = [
    url(r'^movies/$', movies, name="movies"),
    url(r'^movie/(?P<id>[0-9]+)/', movie,  name="movie"),
    url(r'^likeMovie/$', likeMovie, name="likeMovie"),
    url(r'^reviewMovie/(?P<id>[0-9]+)/', reviewMovie, name="reviewMovie"),
    url(r'^deleteReview/', deleteReview, name="deleteReview"),
    url(r'^loadMovies/$', loadMovies, name="loadMovies"),
    url(r'^assignImage/(?P<id>[0-9]+)/', assignImage, name="assignImage"),
    url(r'^rateMovie/', rateMovie, name="rateMovie"),
]
