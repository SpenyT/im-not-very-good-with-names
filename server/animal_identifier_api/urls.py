from django.urls import path
from django.http import HttpResponse

def home(request):
    return HttpResponse("Animal Identifier API is running! ✅")

urlpatterns = [
    # path('admin/', admin.site.urls),  # ← Comment this out
    path('', home),
]
