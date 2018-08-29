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
    Friend_Remove,
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

    path('add/<int:pk>/', Friend_Add.as_view(), name='add'),
    path('unrequest/<int:pk>/', Friend_Unrequest.as_view(), name='unrequest'),
    path('accept/<int:pk>/', Friend_Accept.as_view(), name='accept'),
    path('remove/<int:pk>/', Friend_Remove.as_view(), name='remove'),
    path('unfriend/<int:pk>/', Friend_Unfriend.as_view(), name='unfriend'),

    path('flogic/', Friend_Logic.as_view(), name='friend_logic'),
    path('block/<int:pk>/', Friend_Block.as_view(), name='block'),
    path('unblock/<int:pk>/', Friend_Unblock.as_view(), name='unblock'),

]


