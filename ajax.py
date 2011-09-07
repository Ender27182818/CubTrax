from django.utils import simplejson
from dajaxice.core import dajaxice_functions
from models import *

def get_den_by_long_form(den_type):
	"""Convert a den type in long form, such as 'Wolf' to the short form, 'F'"""
	for d in Den.DEN_TYPES:
		if den_type == d[1]:
			den_type_short = d[0]
	return Den.objects.get(den_type=den_type_short)
	
def myexample(request):
	
	return simplejson.dumps({'message':'Hello from Django Ajax Ice'})
dajaxice_functions.register(myexample)

def add_scout(request, first_name, last_name, birthday, den_type):
	"""Create a scout from the given data, assuming den_type is of the long form, eg 'Wolf', not the short form, eg'F'"""
	den = get_den_by_long_form( den_type )
	new_scout = CubScout.objects.create( first_name=first_name, last_name=last_name, birthday=birthday, den=den )
	return simplejson.dumps({ 'first_name':first_name, 'last_name':last_name, 'birthday':birthday, 'den_type':den_type, 'scout_id':new_scout.id })
dajaxice_functions.register(add_scout)

def remove_scout(request, scout_id):
	CubScout.objects.get(id=scout_id).delete()
	return simplejson.dumps({'scout_id':scout_id})
dajaxice_functions.register(remove_scout)

def edit_scout(request, scout_id, first_name, last_name, birthday, den_type):
	"""Edit the scout with the given scout id to have the given values"""
	den = get_den_by_long_form( den_type )
	scout = CubScout.objects.get(id=scout_id)
	scout.first_name = first_name
	scout.last_name = last_name
	scout.birthday = birthday
	#scout.den = den
	scout.save()
	return simplejson.dumps({ 'scout_id':scout_id, 'first_name':first_name, 'last_name':last_name, 'birthday':birthday, 'den_type':den.get_den_type_display() })
dajaxice_functions.register(edit_scout)
