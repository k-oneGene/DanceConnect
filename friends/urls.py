from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .apps import FriendsConfig


from .views import (
    FriendsListView
)

app_name = FriendsConfig.name

urlpatterns = [
    path('', FriendsListView.as_view(), name="list"),
]