from django.urls import path

from event_manager import views


urlpatterns = [
    path('event/create/', views.EventViewSets.as_view({'post': 'create'}), name='create_event'),
    path('register/', views.RegisterUserAPIView.as_view(), name='register_user')
]