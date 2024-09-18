from django.contrib import admin
from .models import Product, Order, Notification, OfferMail
# Register your models here.
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Notification)
admin.site.register(OfferMail)
