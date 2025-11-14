from django.urls import path, include

urlpatterns = [
    path('api/enrichment/', include('enrichment.urls')),
]
