from django.urls import path
from .consumers import FoodDelibery, SendNotification

websocket_urlpatterns = [
    path('ws/food-delivery/<order_id>/', FoodDelibery.as_asgi()),
    path('ws/send-notification/', SendNotification.as_asgi())
]