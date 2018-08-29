from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import reverse, reverse_lazy



from .apps import ProfilesConfig


from .views import (
    ProfileListView,
    ProfileDetailView,
    ProfileUpdateView,
    SignUpCreateView,
    SignUpProfileCreateView,
    ProfileSettingsView,
    MyPastEventsListView,
    MyFutureEventsListView,
    MyNotificationsView,
    MyNotificationsBoxView,
    login_test_view
)

app_name = ProfilesConfig.name

urlpatterns = [
    path('', ProfileListView.as_view(), name="list"),
    path('<int:pk>/', ProfileDetailView.as_view(), name="detail"),
    path('update/', ProfileUpdateView.as_view(), name="update"),

    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),

    path('password_reset/', auth_views.PasswordResetView.as_view(
                template_name='registration/password_reset_form.html',
                success_url=reverse_lazy('profiles:password_reset_done')
            ),
        name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_email.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('settings/', ProfileSettingsView.as_view(), name="settings"),



    # path('', include('django.contrib.auth.urls')),
    path('signup/', SignUpCreateView.as_view(), name='signup'),
    path('signup-profile/', SignUpProfileCreateView.as_view(), name='profile'),

    path('logintest/', login_test_view),

    path('past_events/', MyPastEventsListView.as_view(), name='my_past'),
    path('future_events/', MyFutureEventsListView.as_view(), name='my_future'),

    path('notifications/', MyNotificationsView.as_view(), name='my_notifications'),
    path('notificationsbox/', MyNotificationsBoxView.as_view(), name='my_notifications_box'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)