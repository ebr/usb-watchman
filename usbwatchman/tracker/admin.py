from django.contrib import admin
from tracker.models import Device, Event

class EventInline(admin.StackedInline):
	model = Event
	extra = 1

class DeviceAdmin(admin.ModelAdmin):
	fields = ['name', 'asset_tag', 'vendor', 'serial', 'model']
	inlines = [EventInline]


admin.site.register(Device, DeviceAdmin)