
def all():
	"""Gets all of the defined awards"""
	return Award._awards_map.values()

def get( id ):
	"""Gets the award with the given ID"""
	id = int(id)
	return Award._awards_map[id]

def get_requirement( id ):
	"""Gets the requirement with the given ID"""
	id = int(id)
	return Requirement._requirements_map[id]

	
class UnicodeConverter():
	"""A simple mix-in that handles converting from Django's __unicode__ convert to a pythonic __str__ converter"""
	def __str__(self):
		return self.__unicode__()
	
class Award(UnicodeConverter):
	"""An award, such as Bobcat, Wolf, an Arrow point or the Swimming Belt Loop"""
	_current_award_id = 0

	_awards_map = {}

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
			self.requirements.append( Requirement( self, *r ) )
		# Save the new award so that we can always access it in the awards list
		Award._awards_map[self.id] = self

	def __unicode__(self):
		return self.name
	def pk(self):
		return self.id

	def db_name(self):
		return "awards.{0}".format(self.name.lower)

class Requirement():
	"""A requirement for an award, such as 'swim 100 meters', or 'paint a picture'"""
	
	# Used to give out unique IDs to each Requirement as its made
	_current_requirement_id = 0

	# Used to store all requirement IDs with their name
	choices_map = []	

	# Used to map ids to Requirements
	_requirements_map = {}

	@staticmethod
	def _get_id():
		"""Returns an available ID number for a new award"""
		requirement_id = Requirement._current_requirement_id
		Requirement._current_requirement_id = requirement_id + 1
		return requirement_id

	def __init__(self, award, name, contents, additional_info="", subordinate_requirements=[]):
		self.id = Requirement._get_id()
		if not isinstance(award, Award):
			raise Exception( "{0} is not an Award".format(award) )
		self.award = award
		self.name = name
		self.contents = contents
		self.additional_info = additional_info
		self.parent_requirement = None
		# First see if the subordinate requirements is a list of Requirements and save it off if so
		self.subordinate_requirements = []
		for sr in subordinate_requirements:
			new_requirement = Requirement( award, *sr )
			new_requirement.parent_requirement = self
			self.subordinate_requirements.append( new_requirement )
		
		Requirement.choices_map.append( (self.id, self.name) )
		Requirement._requirements_map[self.id] = self

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
