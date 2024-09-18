from django.urls import path
from .consumers import FoodDelibery

websocket_urlpatterns = [
    path('ws/food-delivery/', FoodDelibery.as_asgi()),
]