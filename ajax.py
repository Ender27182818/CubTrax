from django.utils import simplejson
from dajaxice.core import dajaxice_functions
from models import *

def myexample(request):
	
	return simplejson.dumps({'message':'Hello World'})
dajaxice_functions.register(myexample)

def add_scout(request, first_name, last_name, birthday, den_type):
	"""Create a scout from the given data, assuming den_type is of the long form, eg 'Wolf', not the short form, eg'F'"""
	for d in Den.DEN_TYPES:
		if den_type is d[1]:
			den_type_short = d[0]
	den = Den.objects.get(den_type='F')
	new_scout = CubScout.objects.create( first_name=first_name, last_name=last_name, birthday=birthday, den=den )
	return simplejson.dumps({ 'first_name':first_name, 'last_name':last_name, 'birthday':birthday, 'den_type':den_type, 'scout_id':new_scout.id })
dajaxice_functions.register(add_scout)

def remove_scout(request, scout_id):
	CubScout.objects.get(id=scout_id).delete()
	return simplejson.dumps({'scout_id':scout_id})
dajaxice_functions.register(remove_scout)
