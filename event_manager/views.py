from django.shortcuts import render
from rest_framework import viewsets

from event_manager import models


# Create your views here.
class EventViewSets(viewsets.ModelViewSet):
    """
    This a viewset that takes json and write the event to the database.
    """
    pass
