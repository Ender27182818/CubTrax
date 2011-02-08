from CubTrax.models import *
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from CubTrax.forms import *
import CubTrax.awards

def test(request):
	return render_to_response('CubTrax/test.html', {'bobcat':CubTrax.awards.bobcat})

def index(request):
	cubs = CubScout.objects.all().order_by('birthday')
	return render_to_response('CubTrax/index.html', {'cubs':cubs}, context_instance=RequestContext(request))

def scout_manager(request):
	return render_to_response('CubTrax/scouts.html', {'scouts':scouts, 'dens':dens}, context_instance=RequestContext(request))

def scouts(request):
	scouts = CubScout.objects.all()
	dens = Den.objects.all()
	den_types = [v for k, v in Den.DEN_TYPES]
	return render_to_response('CubTrax/scouts.html', {'scouts':scouts, 'dens':dens, 'den_types':den_types}, context_instance=RequestContext(request))

def scout_detail(request, scout_id):
	scout = CubScout.objects.get(id=scout_id)
	form = QuickAddAchievementForm(initial={'cub_scout':scout})
	return render_to_response('CubTrax/scout_detail.html', {'scout':scout, 'form':form}, context_instance=RequestContext(request))

def quick_add_accomplishment(request, scout_id):
	if request.method == 'POST':
		form = AddCubScoutForm(request.POST)
		if form.is_valid():
			form.save()
		return HttpResponseRedirect('../')
	else:
		return HttpResponseRedirect('../')
	
def add_scout(request):
	if request.method == 'POST':
		form = AddCubScoutForm(request.POST)
		if form.is_valid():
			new_scout = form.save()
			return HttpResponseRedirect('./added/%d' % new_scout.pk)
	else:
		form = AddCubScoutForm()
	return render_to_response('CubTrax/add_scout.html', {'form': form}, context_instance=RequestContext(request))

def added_scout(request, scout_id):
	scout = CubScout.objects.get(pk=scout_id)
	return render_to_response('CubTrax/added_scout.html', {'scout':scout}, context_instance=RequestContext(request))

def awards(request):
	awards = CubTrax.awards.all()
	return render_to_response('CubTrax/awards.html', {'awards':awards}, context_instance=RequestContext(request))

def award_detail(request, award_id):
	award = CubTrax.awards.get(id=award_id)
	return render_to_response('CubTrax/award_detail.html', {'award':award}, context_instance=RequestContext(request))

def meetings(request):
	meetings = Meeting.objects.all()
	return render_to_response('CubTrax/meetings.html', {'meetings':meetings}, context_instance=RequestContext(request))

def meeting_detail(request, meeting_id):
	meeting = Meeting.objects.get(pk=meeting_id)
	return render_to_response('CubTrax/meeting_detail.html', {'meeting':meeting}, context_instance=RequestContext(request))

def add_meeting(request):
	if request.method == 'POST':
		form = AddMeetingForm(request.POST)
		if form.is_valid():
			new_meeting = form.save()
			for scout in new_meeting.attendees.all():
				for req in new_meeting.requirements.all():
					Achievement.objects.create(cub_scout=scout, requirement=req, date=new_meeting.date, meeting=new_meeting)
			return HttpResponseRedirect('./added/%d' % new_meeting.pk)
	else:
		form = AddMeetingForm()
	return render_to_response('CubTrax/add_meeting.html', {'form': form}, context_instance=RequestContext(request))

def added_meeting(request, meeting_id):
	meeting = Meeting.objects.get(pk=meeting_id)
	return render_to_response('CubTrax/added_meeting.html', {'meeting':meeting}, context_instance=RequestContext(request))
