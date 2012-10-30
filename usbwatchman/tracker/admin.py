from django.contrib import admin
from tracker.models import Device, Event

class EventInline(admin.TabularInline):
	model = Event
	extra = 1

class DeviceAdmin(admin.ModelAdmin):
	list_display = ('name', 'asset_tag', 'vendor', 'serial', 'model', 'connected')
	inlines = [EventInline]
	list_filter = ['model']


admin.site.register(Device, DeviceAdmin)