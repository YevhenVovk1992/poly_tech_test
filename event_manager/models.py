import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from event_manager.validators import DateValidator


# Create your models here.
class UUIDModel(models.Model):
    """
    An abstract method where the primary key is not changed
    but an ID column is added to be used in the foreign keys of the models.
    """
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True


class EventType(models.Model):
    """
    A model that specifies the type of event.
    """
    name = models.CharField(max_length=254, null=False)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ('id', )
        verbose_name = 'Type of the event'
        verbose_name_plural = 'Types of events'


class Event(UUIDModel):
    """
    The model that describes the event according to the specification.
    """
    user = models.ForeignKey(User, null=False, related_name='user', on_delete=models.SET('User was delete'))
    event_type = models.ForeignKey(EventType, null=False, related_name='event_type', on_delete=models.CASCADE)
    info = models.JSONField(null=True)
    timestamp = models.DateTimeField(null=False, validators=[DateValidator.timestamp_validator])
    created_at = models.DateTimeField(null=False, default=timezone.now())

    class Meta:
        ordering = ('created_at', )
        verbose_name = 'Event'
        verbose_name_plural = 'Events'


