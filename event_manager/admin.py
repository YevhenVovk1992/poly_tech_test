from django.contrib import admin
from .models import Event, EventType


# Register your models here.
class EventAdmin(admin.ModelAdmin):
    list_display = ('pkid', 'id', 'user', 'event_type', 'info', 'timestamp', 'created_at')
    list_filter = ('event_type', 'timestamp')
    list_display_links = ('pkid', 'id', 'info', 'timestamp', 'created_at')


class EventTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


admin.site.register(Event, EventAdmin)
admin.site.register(EventType, EventTypeAdmin)
