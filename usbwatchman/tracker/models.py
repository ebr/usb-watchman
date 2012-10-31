from django.db import models
from django.utils import timezone

# Create your models here.

class Device(models.Model):
	name = models.CharField(max_length=50)
	serial = models.CharField(max_length=50)
	vendor = models.CharField(max_length=50)
	model = models.CharField(max_length=50)
	asset_tag = models.CharField(max_length=50)
	
	def __unicode__(self):
		return self.name
		
	def last_event(self):
		if self.has_events():
			return self.event_set.latest()
		else:
			return "Device has no events" 
		
	def current_state(self):
		if self.has_events():
			return str(self.event_set.latest('timestamp').event_type) ## This uses the last state change in database to determine current state. Is there a better way?
		else:
			return "Device has no events"
		
	def connected(self):
		return self.current_state() == "Added"
		## assumes this is sanitized by current_state()
		
	connected.boolean = True ## to let the template know that it should show as a check/uncheck icon
	
	def connect(self):
		self.event_set.create(event_type='Added', timestamp=timezone.now())

	def disconnect(self):
		self.event_set.create(event_type='Removed', timestamp=timezone.now())
		
	def register(self):
		self.event_set.create(event_type='Registered', timestamp=timezone.now())
	

	def has_events(self):
		return len(self.event_set.all()) > 0

class Event(models.Model):
	device = models.ForeignKey(Device)
	timestamp = models.DateTimeField()
	event_type = models.CharField(max_length=20)
	
	def __unicode__(self):
# 		return (self.timestamp.isoformat() + ": " + self.event_type + ": " + self.device.name )
# 		return (self.event_type + " " + self.timestamp.strftime('%Y/%m/%d %H:%M:%S'))
		return "Event " + str(self.id)		
		
	get_latest_by = 'timestamp'

