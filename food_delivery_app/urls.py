from django.urls import path
from . import views


urlpatterns = [
    path('', views.Home, name='home'),
    path('order-api/', views.OrderApi),
    path('order-list/', views.OrderList, name='order_list'),
    path('order-view/<id>/', views.OrderView, name='order_view'),
    path('user-list/', views.UserList, name='user_list'),
    path('email-send/', views.SendMail, name='send_mail')
]