# -*- coding: utf-8 -*-

from django.contrib import admin
from models import *

class UserProfieAdmin(admin.ModelAdmin):
	fields = ('user', 'userType', 'follows', 'groups', 'groupsAdministrated', 'favMovies', 'favPersons')
	filter_horizontal = ('follows', 'groups', 'groupsAdministrated', 'favMovies', 'favPersons')

admin.site.register(UserType)
admin.site.register(UserProfile,  UserProfieAdmin)
