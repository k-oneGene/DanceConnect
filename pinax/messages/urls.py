from django.conf.urls import url

from . import views

app_name = "pinax_messages"

urlpatterns = [
    url(r"^inbox/$", views.InboxView.as_view(),
        name="inbox"),
    url(r"^chat/(?P<pk>\d+)/$", views.ChatUpdateView.as_view(),
        name="chat_update"),
    url(r"^chat/$", views.ChatView.as_view(),
        name="chat"),
    url(r"^create/$", views.MessageCreateView.as_view(),
        name="message_create"),
    url(r"^create/(?P<user_id>\d+)/$", views.MessageCreateView.as_view(),
        name="message_user_create"),
    url(r"^thread/(?P<pk>\d+)/$", views.ThreadView.as_view(),
        name="thread_detail"),
    url(r"^thread/(?P<pk>\d+)/delete/$", views.ThreadDeleteView.as_view(),
        name="thread_delete"),

    url(r'^messages/$', views.Messages, name='messages'),

    url(
        r'^thread-autocomplete/$',
        views.ThreadAutocomplete.as_view(),
        name='thread-autocomplete',
    ),

    url(
        r'^user-autocomplete/$',
        views.UserAutocomplete.as_view(),
        name='user-autocomplete',
    ),

]
