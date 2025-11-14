from django.urls import path
from .views import ping

app_name = 'classifier'

urlpatterns = [
    path("ping/", ping, name="ping"),
]
