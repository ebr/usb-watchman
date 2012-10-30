#!/usr/bin/env python
import os
import sys
import pyudev
from models import Device, Event
from django.utils import timezone

context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem='usb', device_type='usb_device')

def device_data(raw_data):
	''' Accept a device. Return a tuple of attributes of given device. 
		Clean up all strings in the process and make pretty.
	'''
	
	vendor = raw_data['ID_VENDOR'].replace('_',' ')
	model = raw_data['ID_MODEL'].replace('_',' ')
	try:
		serial = raw_data['ID_SERIAL_SHORT']
	except:
		serial = raw_data['ID_SERIAL']
	return vendor, model, serial 


def log_event(device, event_type):

	device.event_set.create(timestamp=timezone.now(), event_type = event_type)

	
def get_device(device_data):
	'''get the device based on given data. if device is not found, create it and save to database. Also log a "new device" event. then return the device.'''

	try:
		d = Device.objects.get(serial=device_data[2])
	except:
		initial_name = device_data[0] + ' ' +  device_data[1] + ' ' + device_data[2]
		d = Device( name = initial_name, vendor = device_data[0], model = device_data[1], serial = device_data[2] )
		d.save()
		log_event(d, 'Registered')

	return d
	
def process_device_event(raw_data):
	
	clean_data=device_data(raw_data)
	
	d = get_device(clean_data)
	
	log_event(d, raw_data.action)
	


observer = pyudev.MonitorObserver(monitor, callback=process_device_event, name='monitor-observer')
observer.daemon = False


if __name__ == "__main__":
    
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "usbwatchman.settings")
    
    observer.start()