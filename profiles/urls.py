from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .apps import ProfilesConfig


from .views import (
    ProfileListView,
    ProfileDetailView,
    ProfileUpdateView,
    SignUpCreateView,
    SignUpProfileCreateView,
    MyPastEventsListView,
    MyFutureEventsListView,
    login_test_view
)

app_name = ProfilesConfig.name

urlpatterns = [
    path('', ProfileListView.as_view(), name="list"),
    path('<int:pk>/', ProfileDetailView.as_view(), name="detail"),
    path('update/', ProfileUpdateView.as_view(), name="update"),

    path('', include('django.contrib.auth.urls')),
    path('signup/', SignUpCreateView.as_view(), name='signup'),
    path('signup-profile/', SignUpProfileCreateView.as_view(), name='profile'),
    path('logintest/', login_test_view),

    path('past_events/', MyPastEventsListView.as_view(), name='my_past'),
    path('future_events/', MyFutureEventsListView.as_view(), name='my_future'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)