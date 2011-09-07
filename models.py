from django.db import models
from datetime import date, timedelta
import awards

class AwardField(models.Field):
	"""A field to contain a reference to a given award"""
	description = "A reference to an award"
	__metaclass__ = models.SubfieldBase

	def __init__(self, *args, **kwargs):
		kwargs['max_length'] = 100
		super(AwardField, self).__init__(*args, **kwargs)

	def to_python(self, value):
		if isinstance(value, awards.Award):
			return value

		# The string case
		if isinstance(value, basestring):
			return eval(value)

	def get_prep_value(self, value):
		return value.db_name()

	def get_prep_lookup(self, lookup_type, value):
		if lookup_type == 'exact':
			return self.get_prep_value(value)
		elif lookup_type == 'in':
			return [self.get_prep_value(v) for v in value]
		else:
			raise TypeError('Lookup type {0} not supported'.format(lookup_type))
	def get_internal_type(self):
		return 'CharField'

class Person( models.Model ):
	"""A person"""
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)

	def __unicode__(self):
		return self.first_name + " " + self.last_name
	def Name(self):
		return "%s %s" % (self.first_name, self.last_name)
	class Meta:
		abstract = True

class Adult( Person ):
	"""An adult, usually a leader"""
	pass
	
class Pack( models.Model ):
	number = models.IntegerField()
	
	def __unicode__(self):
		return "Pack #%d" % self.number


class Den( models.Model ):
	"""A cub scout den"""
	DEN_TYPES = (
		(u'T', u'Tiger'),
		(u'F', u'Wolf'),
		(u'B', u'Bear'),
		(u'W', u'WeBeLoS'),
	)
	den_type = models.CharField(max_length=1, choices=DEN_TYPES)
	pack = models.ForeignKey( Pack )
	leader = models.ForeignKey( Adult )
	
	def __unicode__(self):
		return "%s den of pack %s" % (self.get_den_type_display(), str(self.pack))



class CubScout( Person ):
	"""A cub scout"""
	birthday = models.DateField( 'birthday', blank=True, null=True )
	den = models.ForeignKey( Den )
	def get_current_award(self):
		return awards.get(0)
	
	def GetLastBirthday(self):
		"""Gets the last birthday"""
		if( self.birthday == None ):
			return None
		this_year_birthday = date( date.today().year, self.birthday.month, self.birthday.day )
		if( this_year_birthday < date.today() ):
			return this_year_birthday
		else:
			return this_year_birthday - timedelta( 365 )

	def GetNextBirthday(self):
		"""Gets the next birthday for this person"""
		if( self.birthday == None ):
			return None
		else:
			return self.GetLastBirthday() + timedelta( 365 )

	def GetBirthdayPercentage(self):
		"""Gets the percentage of time completed to their next birthday"""
		if( self.birthday == None ):
			return 0
		last_birthday = self.GetLastBirthday()
		time_passed = date.today() - last_birthday
		return (time_passed.days / 365.0)
	
	def GetBirthdayPercentageInt(self):
		"""Gets the percentage of time completed to their next birthday as an int from 0-100"""
		return int( self.GetBirthdayPercentage() * 100 )
	
	def GetBirthdayString(self):
		"""Gets the birthday as a month/day pair, like 'Jan 1'"""
		if self.birthday:
			return self.birthday.strftime("%b %m")
		else:
			return "?"

	def LatestAchievements(self, n=5):
		"""Gets the n latest achievements"""
		#achievements = self.achievement_set.order_by( 'date' )[:n]
		meetings = self.meeting_set.order_by( 'date' )
		reqs = []
		for m in meetings:
			for r in m.requirements.all():
				reqs.append(r)
				if( len(reqs) == n ):
					return reqs
		return reqs

	def ToDo(self, n=5):
		"""Gets the n requirements for the current award that have yet to be done"""
		return None #Requirement.objects.filter(award=self.get_current_award()).exclude(cubscout=self)[:n]

class Requirement( models.Model ):
	"""A thin wrapper around awards.Requirement"""
	requirement_id = models.IntegerField()
	def __unicode__(self):
		return awards.get_requirement(self.requirement_id).name
	def requirement(self):
		return awards.get_requirement(self.requirement_id)

class Meeting( models.Model ):
	"""Represents a meeting where something was accomplished for the scouts"""
	attendees = models.ManyToManyField(CubScout)
	leaders = models.ManyToManyField(Adult)
	date = models.DateField()
	location = models.CharField(max_length=200)
	notes = models.TextField()
	requirements = models.ManyToManyField( Requirement, blank=True )
	def __unicode__(self):
		return "Meeting on %s at %s" % (self.date, self.location)

class Achievement( models.Model ):
	"""An achievement that a scout has performed which fulfills a requirement"""
	date = models.DateField()
	meeting = models.ForeignKey(Meeting, null=True, blank=True)
	scout = models.ForeignKey(CubScout)
	def __unicode__(self):
		return "%s did %s on %s" % (str(self.cub_scout), self.requirement.name, self.date)

