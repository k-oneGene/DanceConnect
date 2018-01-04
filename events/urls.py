from django.urls import path
from .apps import EventsConfig

from .views import (
    EventListView,
    EventDetailView,
    CategoryListView,
    CategoryListInfoListView
)

app_name = EventsConfig.name

urlpatterns = [
    path('', EventListView.as_view(), name="list"),
    path('<int:pk>/', EventDetailView.as_view(), name="detail"),
    path('category/', CategoryListView.as_view(), name="category"),
    path('category/<slug:slug>/', CategoryListInfoListView.as_view(), name="category-list-info"),
]
