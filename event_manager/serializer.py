from django.contrib.auth.models import User
from rest_framework import serializers

from event_manager import models


class EventTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = models.EventType
        fields = ('name', )


class EventSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='pk')
    event_type = serializers.SlugRelatedField(queryset=models.EventType.objects.all(), slug_field='name')
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = models.Event
        fields = ('user', 'event_type', 'info', 'timestamp', 'created_at')

