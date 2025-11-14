from django.urls import path
from . import views

app_name = 'enrichment'

urlpatterns = [
    path('ping/', views.ping, name='ping'),
]
