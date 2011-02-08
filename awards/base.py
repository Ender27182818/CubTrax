_awards_map = {}

def all():
	"""Gets all of the defined awards"""
	return _awards_map.values()

def get( id ):
	"""Gets the award with the given ID"""
	id = int(id)


	return _awards_map[id]

class UnicodeConverter():
	"""A simple mix-in that handles converting from Django's __unicode__ convert to a pythonic __str__ converter"""
	def __str__(self):
		return self.__unicode__()
	
class Award(UnicodeConverter):
	"""An award, such as Bobcat, Wolf, an Arrow point or the Swimming Belt Loop"""
	_current_award_id = 1

	@staticmethod
	def _get_id():
		"""Returns an available ID number for a new award"""
		award_id = Award._current_award_id
		Award._current_award_id = award_id + 1
		return award_id

	def __init__(self, name, reqs):
		"""Create a new award with an auto-generated ID"""
		self.id = Award._get_id()
		self.name = name
		self.requirements = []
		for r in reqs:
			self.requirements.append( Requirement.fromarray( self, *r ) )
		# Save the new award so that we can always access it in the awards list
		_awards_map[self.id] = self

	def __unicode__(self):
		return self.name
	def pk(self):
		return self.id

	def db_name(self):
		return "awards.{0}".format(self.name.lower)

class Requirement():
	"""A requirement for an award, such as 'swim 100 meters', or 'paint a picture'"""

	@classmethod
	def fromarray(cls, *args):
		if( len( args ) < 3 ):
			raise Exception( "{0} has {1} arguments - need at least 3".format(args, len(args)) )
		new_req = cls(args[0], args[1], args[2])
		if( len(args) > 3 ):
			new_req.additional_info = args[3]
		if( len(args) > 4 and not isinstance(args[4], basestring)):
			new_req.subordinate_requirements = []
			for r in args[4]:
				new_req.subordinate_requirements.append( Requirement.fromarray( *r ) )
		return new_req

	def __init__(self, award, name, contents, additional_info="", subordinate_requirements=[]):
		self.award = award
		self.name = name
		self.contents = contents
		self.additional_info = additional_info
		self.subordinate_requirements = subordinate_requirements

	def __unicode__(self):
		return "{0} - {1}".format( self.award.name, self.name )

	def to_li(self):
		sub_string = ""
		if( self.subordinate_requirements ):
			sub_string = "<ul>"
			for sub_req in self.subordinate_requirements:
				sub_string += sub_req.to_li()
			sub_string += "</ul>"
		return "<li>{0} - {1}{2}</li>".format( self.name, self.contents, sub_string )
