from django.urls import path
from .apps import EventsConfig

from .views import (
    EventListView,
    EventDetailView,
    EventCreateView,
    EventUpdateView,
    EventDeleteView,
    CategoryListView,
    CategoryListInfoListView,
    EventGoingToggle
)

app_name = EventsConfig.name

urlpatterns = [
    path('', EventListView.as_view(), name="list"),
    path('<int:pk>/', EventDetailView.as_view(), name="detail"),
    path('create/', EventCreateView.as_view(), name="create"),
    path('edit/<int:pk>', EventUpdateView.as_view(), name="edit"),
    path('delete/<int:pk>', EventDeleteView.as_view(), name="delete"),
    path('category/', CategoryListView.as_view(), name="category"),
    path('category/<slug:slug>/', CategoryListInfoListView.as_view(), name="category-list-info"),

    path('going/', EventGoingToggle.as_view(), name='going'),
]

