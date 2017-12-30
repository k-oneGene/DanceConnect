from django.urls import path
from .apps import EventsConfig

from .views import (
    EventListView,
    EventDetailView
)

app_name = EventsConfig.name

urlpatterns = [
    path('', EventListView.as_view(), name="list"),
    path('<int:pk>/', EventDetailView.as_view(), name="detail"),
]
