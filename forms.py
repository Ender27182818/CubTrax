from django import forms
from CubTrax.models import *

class AddCubScoutForm(forms.ModelForm):
	class Meta:
		model = CubScout


class AddMeetingForm(forms.ModelForm):
	class Meta:
		model = Meeting
	
class QuickAddAchievementForm(forms.ModelForm):
	class Meta:
		model = Achievement
		exclude = ('meeting', 'cub_scout')
