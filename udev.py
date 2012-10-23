import pyudev
from time import strftime

current_devices={}


context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem='usb', device_type='usb_device')


def timestamp():
	return strftime('%Y/%m/%d %H:%M:%S')


def decode_device_info(device):
	''' Accept a device. Return a dict of attributes of given device. 
		Clean up all strings in the process and make pretty.
	'''
	
	vendor = device['ID_VENDOR'].replace('_',' ')
	model = device['ID_MODEL'].replace('_',' ')
	serial = device['ID_SERIAL_SHORT']
	
	return({'vendor':vendor, 'model':model, 'serial':serial})


def log_device_event(device):
	'''Add or remove device to/from the dict of currently plugged in devices. Return the dict.
	'''
	global current_devices
	
	devname = device['DEVNAME']
	
	if device.action == 'add':
		current_devices[devname] = (decode_device_info(device), timestamp())
	if device.action == 'remove':
		try:
			del current_devices[devname]
		except KeyError:
			print '\n'
		
	return(current_devices)
	

def formatted_listing(device_dict):
	''' Print a nicely formatted listing of devices currently in the device_dict 
	'''

	print('\n' + '-'*15 + ' Currently Plugged In: ' + '-'*15)
	for device_record in device_dict.keys():
		print("{0[vendor]} {0[model]}: {0[serial]}".format(device_dict[device_record][0]))

def print_device_event(device):
	'''Print details of a device added or removed
	'''
	
	global current_devices
	
	#print('background event {0.action}: {0.device_type}'.format(device))
	#print(dir(device))
	#print(list(device.items()))
	if device.action == 'add':
		print(timestamp()+" | Device {0[ID_VENDOR]} {0[ID_MODEL]} with serial number {0[ID_SERIAL]} was plugged in. ----- {0[DEVNAME]}".format(device))
	if device.action == 'remove':
		#print(timestamp()+" | Device {0[vendor]} {0[model]} with serial number {0[serial]} was removed".format(current_devices[device[devname][1]]))
		print("device removed")
	
	formatted_listing(current_devices)
	
def process_device_event(device):
	
	
	log_device_event(device)
	print_device_event(device)
	


observer = pyudev.MonitorObserver(monitor, callback=process_device_event, name='monitor-observer')
observer.daemon = False


if __name__ == '__main__':
	
	observer.start()

