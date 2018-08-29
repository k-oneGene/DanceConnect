from django.urls import path
from .apps import PaymentsConfig

from .views import (
    ipn_listender,

)

app_name = PaymentsConfig.name

urlpatterns = [
    path('ipn', ipn_listender, name="ipn"),

]

