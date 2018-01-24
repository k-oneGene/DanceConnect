from django.urls import path

from .apps import VendersConfig


from .views import (
    VenderListView,
    VenderDetailView,
)

app_name = VendersConfig.name

urlpatterns = [
    path('', VenderListView.as_view(), name="list"),
    path('<int:pk>/', VenderDetailView.as_view(), name="detail"),
    # path('update/', ProfileUpdateView.as_view(), name="update"),
]