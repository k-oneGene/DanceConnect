from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .apps import FriendsConfig


from .views import (
    FriendsListView,
    FriendsRequestedListView,
    FriendsMyRequestsListView,
    FriendsBlockedListView,

    Friend_Add,
    Friend_Unrequest,
    Friend_Accept,
    Friend_Unfriend,

    Friend_Block,
    Friend_Unblock,
    Friend_Logic,

)

app_name = FriendsConfig.name

urlpatterns = [
    path('', FriendsListView.as_view(), name="friends"),
    path('requests/', FriendsRequestedListView.as_view(), name="requests"),
    path('sent_requests/', FriendsMyRequestsListView.as_view(), name="my_requests"),
    path('blocked/', FriendsBlockedListView.as_view(), name="blocked"),

    path('add/', Friend_Add.as_view(), name='add'),
    path('unrequest/', Friend_Unrequest.as_view(), name='unrequest'),
    path('accept/', Friend_Accept.as_view(), name='accept'),
    path('unfriend/', Friend_Unfriend.as_view(), name='unfriend'),

    path('flogic/', Friend_Logic.as_view(), name='friend_logic'),
    path('block/', Friend_Block.as_view(), name='block'),
    path('unblock/', Friend_Unblock.as_view(), name='unblock'),


]


