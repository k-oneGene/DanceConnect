from django.urls import path
from .apps import SearchConfig

from .views import (
    SearchEventsListview,
    SearchProfilesListview
)

app_name = SearchConfig.name

urlpatterns = [
    path('events/', SearchEventsListview.as_view(), name="SearchEvents"),
    path('profiles/', SearchProfilesListview.as_view(), name="SearchProfiles"),
]
