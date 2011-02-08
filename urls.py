from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('CubTrax.views',
	(r'^$', 'index'),
	(r'^scouts/$', 'scouts'),
	(r'^scouts/(?P<scout_id>\d+)/$', 'scout_detail'),
	(r'^scouts/(?P<scout_id>\d+)/quick_add_accomplishment', 'quick_add_accomplishment'),		
	(r'^scouts/add$', 'add_scout'),
	(r'^scouts/added/(?P<scout_id>\d+)/$', 'added_scout'),

	(r'^awards/$', 'awards'),
	(r'^awards/(?P<award_id>\d+)/$', 'award_detail'),
	(r'^meetings/$', 'meetings'),
	(r'^meetings/(?P<meeting_id>\d+)/$', 'meeting_detail'),
	(r'^meetings/add$', 'add_meeting'),
	(r'^meetings/added/(?P<meeting_id>\d+)/$', 'added_meeting'),
	
	(r'^test/$', 'test'),
)
