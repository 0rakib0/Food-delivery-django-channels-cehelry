from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from food_delivery_app import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home, name='home')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)