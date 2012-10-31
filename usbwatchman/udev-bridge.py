#!/usr/bin/env python
import os
import sys

sys.path.append('/usr/bin/python')
os.environ['DJANGO_SETTINGS_MODULE'] = 'usbwatchman.settings'

import pyudev
from django.utils import timezone

from tracker.models import Device, Event

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


def get_device(device_data):
	''' return the device from database based on given data. 
		if device is not found, create it.'''

	try:
		d = Device.objects.get(serial=device_data[2])
	except:
		d = new_device(device_data)
				
	return d
	
def new_device(device_data):
	'''given device data, create a new Device and enter it into database. Also log an event of "new device" type'''
	
	initial_name = device_data[0] + ' ' +  device_data[1] + ' ' + device_data[2]
	d = Device( name = initial_name, vendor = device_data[0], model = device_data[1], serial = device_data[2] )
	d.save()
	d.register()
	
	return d
	
	
def process_device_event(raw_data):

	if raw_data.action == 'add':
		clean_data=device_data(raw_data)
		d = get_device(clean_data)
		d.connect()
	elif raw_data.action == "remove":
		print raw_data	


observer = pyudev.MonitorObserver(monitor, callback=process_device_event, name='monitor-observer')
observer.daemon = False


if __name__ == "__main__":
        
    observer.start()