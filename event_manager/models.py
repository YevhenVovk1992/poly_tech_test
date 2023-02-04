import datetime
import uuid

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class UUIDModel(models.Model):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True


class EventType(models.Model):
    name = models.CharField(max_length=254, null=False)

    class Meta:
        verbose_name = 'Type of the event'


class Event(UUIDModel):
    user = models.ForeignKey(User, null=False, related_name='user', on_delete=models.SET('User was delete'))
    event_type = models.ForeignKey(EventType, null=False, related_name='event_type', on_delete=models.CASCADE)
    info = models.JSONField(null=True)
    timestamp = models.DateTimeField(null=True)
    created_at = models.DateTimeField(null=False, default=datetime.datetime.now())

    class Meta:
        ordering = ['event_type', 'timestamp']
        verbose_name = 'Event'


