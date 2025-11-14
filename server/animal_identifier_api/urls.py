from django.urls import path, include

urlpatterns = [
    path('api/classify/', include('classifier.urls')),
    path('api/enrichment/', include('enrichment.urls')),
]
