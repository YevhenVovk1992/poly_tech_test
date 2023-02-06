from django.contrib import admin
from rest_framework.authtoken.admin import TokenAdmin

from .models import Event, EventType


# Register your models here.
TokenAdmin.raw_id_fields = ['user']


class EventAdmin(admin.ModelAdmin):
    list_display = ('pkid', 'id', 'user', 'event_type', 'info', 'timestamp', 'created_at')
    list_filter = ('event_type', 'timestamp')
    list_display_links = ('pkid', 'id', 'info', 'timestamp', 'created_at')


class EventTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


admin.site.register(Event, EventAdmin)
admin.site.register(EventType, EventTypeAdmin)
