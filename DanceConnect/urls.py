"""DanceConnect URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path


from .views import HomeView

# from .settings import DEBUG


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', HomeView.as_view(), name="home"),
    path('events/', include('events.urls', namespace='events')),
    path('profiles/', include('profiles.urls', namespace='profiles')),
    path('search/', include('search.urls', namespace='search')),

    # path('profiles/', include('django.contrib.auth.urls')), # TODO: I remember fixing this issue before with another url. Maybe It was different issue?


]

# if DEBUG:
#     import debug_toolbar
#     urlpatterns = [
#                       re_path(r'__debug__/', include(debug_toolbar.urls)),
#                   ] + urlpatterns
