from django.urls import path
from .consumers import FoodDelibery

websocket_urlpatterns = [
    path('ws/food-delivery/<order_id>/', FoodDelibery.as_asgi()),
]