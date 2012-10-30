from django.db import models

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
		return self.event_set.latest('timestamp')
		
	def current_state(self):
		return str(self.event_set.latest('timestamp').event_type) ## This uses the last state change in database to determine current state. Is there a better way?
		
	def connected(self):
		return self.current_state() == "Connected"
		
	connected.boolean = True

	
class Event(models.Model):
	device = models.ForeignKey(Device)
	timestamp = models.DateTimeField()
	event_type = models.CharField(max_length=20)
	
	def __unicode__(self):
# 		return (self.timestamp.isoformat() + ": " + self.event_type + ": " + self.device.name )
		return (self.event_type + " " + self.timestamp.isoformat())
	 