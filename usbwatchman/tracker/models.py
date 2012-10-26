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
	
class Event(models.Model):
	device = models.ForeignKey(Device)
	timestamp = models.DateTimeField()
	event_type = models.CharField(max_length=20)
	
	def __unicode__(self):
		return (self.timestamp.isoformat() + ": " + self.event_type + ": " + self.device.name )
	 