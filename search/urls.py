from django.urls import path
from .apps import SearchConfig

from .views import (
    SearchHomeView,
    SearchEventsListview,
    SearchProfilesListview,
    SearchTeachersListview,
    AdvanceSearchEventsListView,
    SearchFestivalsListView,
    AdvanceSearchFestivalsListView
)

app_name = SearchConfig.name

urlpatterns = [
    path('', SearchHomeView.as_view(), name="home"),
    path('events/', SearchEventsListview.as_view(), name="events"),
    path('events-advance/', AdvanceSearchEventsListView.as_view(), name="events-advance"),
    path('festivals/', SearchFestivalsListView.as_view(), name="festivals"),
    path('festivals-advance/', AdvanceSearchFestivalsListView.as_view(), name="festivals-advance"),
    path('profiles/', SearchProfilesListview.as_view(), name="profiles"),
    path('teachers/', SearchTeachersListview.as_view(), name="teachers"),
]

