from django.utils import simplejson
from dajaxice.core import dajaxice_functions
from models import *

def myexample(request):
	
	return simplejson.dumps({'message':'Hello World'})
dajaxice_functions.register(myexample)

def add_scout(request, name, den_id, tags):
	den = Den.objects.get(id=den_id)
	new_substance = CubScout.objects.create( name=name, den=den )
	return simplejson.dumps({'name':name, 'den':den, 'tags':''})
dajaxice_functions.register(add_scout)

def remove_scout(request, scout_id):
	CubScout.objects.get(id=scout_id).delete()
	return simplejson.dumps({'name':name})
dajaxice_functions.register(remove_scout)
