from django.urls import path
from .apps import SearchConfig

from .views import (
    SearchHomeView,
    SearchEventsListview,
    SearchProfilesListview,
    AdvanceSearchEventsListView
)

app_name = SearchConfig.name

urlpatterns = [
    path('', SearchHomeView.as_view(), name="home"),
    path('events/', SearchEventsListview.as_view(), name="events"),
    path('events-advance/', AdvanceSearchEventsListView.as_view(), name="events-advance"),
    path('profiles/', SearchProfilesListview.as_view(), name="profiles"),
]
