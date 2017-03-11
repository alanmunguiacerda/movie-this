from django import template
from Reviews.models import *

register = template.Library()

@register.filter(name='reviewRate')
def reviewRate(arg1, arg2):
	if arg2 != None:
		return ReviewRate.getUserReviewRate(arg1, arg2)
	else:
		return 0
