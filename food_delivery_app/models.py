from django.db import models
from django.contrib.auth.models import User
import string
import random
# Create your models here.

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class Product(models.Model):
    title = models.CharField(max_length=260)
    details = models.TextField()
    image = models.ImageField(upload_to='products')
    price = models.PositiveIntegerField()
    post_date = models.DateTimeField()
    is_post = models.BooleanField(default=False)
    
    
    def __str__(self) -> str:
        return self.title
    
    
OrderStatus = (
    ('order_receive', 'Order Receive'),
    ('breking', 'Breking'),
    ('breked', 'Breked'),
    ('out_of_delivery', 'Out Of Delivery'),
    ('customar_receive', 'Customar Receive')
)
    
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=120, blank=True, null=True)
    total_amount = models.IntegerField(default=0)
    order_status = models.CharField(max_length=120, choices=OrderStatus, default='order_receive')
    
    
    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = id_generator()
        
        super(Order, self).save(*args, **kwargs)
        
    
    def __str__(self) -> str:
        return self.item.title
    

class Notification(models.Model):
    notification = models.CharField(max_length=260),
    notification_title = models.CharField(max_length=120)
    schedule_date = models.DateTimeField()
    is_sent = models.BooleanField(default=False)
    
    
    def __str__(self) -> str:
        return self.notification
    

class OfferMail(models.Model):
    mail_subject = models.CharField(max_length=120)
    email = models.TextField()
    schedule_date = models.DateTimeField()
    is_sent = models.BooleanField(default=False)
    
    
    def __str__(self) -> str:
        return self.mail_subject