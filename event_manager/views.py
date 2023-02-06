from rest_framework import viewsets, mixins, status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from event_manager import models, serializer


# Create your views here.
class EventViewSets(viewsets.GenericViewSet,
                    mixins.CreateModelMixin):
    """
    This is a viewset that takes json and write the event to the database.
    There is creating the event type if it not in the database.
    """
    queryset = models.Event.objects.all()
    serializer_class = serializer.EventSerializer
    permission_classes = (IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        data = request.data
        data.update({'user': request.user.id, })
        event_type_name = data.get('event_type')
        check_event_type = models.EventType.objects.filter(name=event_type_name).count()
        if not check_event_type:
            event_type_serializer = serializer.EventTypeSerializer(data={'name': event_type_name, })
            event_type_serializer.is_valid(raise_exception=True)
            event_type_serializer.save()
        model_serializer = self.get_serializer(data=data)
        model_serializer.is_valid(raise_exception=True)
        self.perform_create(model_serializer)
        headers = self.get_success_headers(model_serializer.data)
        return Response(model_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = serializer.RegisterSerializer
