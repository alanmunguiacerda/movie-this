# -*- encoding: utf-8 -*-
import json

from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from Movies.models import *
from Images.models import *
from Users.models import *
from Persons.models import *
from moviethis.commons.shortcuts import get_or_none

# TODO: rate system.

def people(request):
	context = {
        'pageName': 'People',
        'pageUrl': '/persons',
	}
	context['bigImage'] = DefaultImage.objects.get(name='logo')

	persons_list = Person.objects.all()
	paginator = Paginator(persons_list, 12)

	page = request.GET.get('page')

	try:
		context['persons'] = paginator.page(page)
	except PageNotAnInteger:
		context['persons'] = paginator.page(1)
	except EmptyPage:
		context['persons'] = paginator.page(paginator.num_pages)
	return render(request, 'persons.html', context)

def person(request, id):
	context = {}
	context['person'] = get_or_none(Person, id=id)
	context['rolRelations'] = RolRelation.objects.filter(person=context['person'])
	context['roles'] = Rol.objects.filter(rolRelation__in = context['rolRelations'])
	print(context['roles'])
	return render(request, 'person.html', context )

@login_required(login_url="/")
def likePerson(request):
	context = {}

	if request.method == 'POST':
		userProfile = UserProfile.objects.get(user=request.user)
		id = request.POST.get('id', None)
		person = get_or_none(Person, id = id)

		if person in userProfile.favPersons.all():
			context['quitar'] = 'text-red-color'
			context['poner'] = 'text-primary-color'
			context['remove'] = '1'
			userProfile.removePerson(person)
		else:
			context['poner'] = 'text-red-color'
			context['quitar'] = 'text-primary-color'
			context['remove'] = '0'
			userProfile.addPerson(person)
		context['id'] = '{!s}'.format(id)
		context['personName'] = person.__str__()
	return HttpResponse(json.dumps(context), content_type='application/json')
