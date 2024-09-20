from django.db import models
from django.contrib.auth.models import User
import string
import random
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from django.dispatch import receiver
from django.db.models.signals import post_save
from django_celery_beat.models import PeriodicTask, CrontabSchedule
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
    
    
    @staticmethod
    def get_percentage(id):
        instance = Order.objects.filter(id=id).first()
        
        progres_percentage = 0  
        if instance.order_status == 'order_receive':
            progres_percentage = 20
        
        if instance.order_status == 'breking':
            progres_percentage = 40
        
        if instance.order_status == 'breked':
            progres_percentage = 60
        
        if instance.order_status == 'out_of_delivery':
            progres_percentage = 80
            
        if instance.order_status == 'customar_receive':
            progres_percentage = 100
            
        return progres_percentage
    

class Notification(models.Model):
    notification = models.CharField(max_length=260),
    notification_title = models.CharField(max_length=120)
    schedule_date = models.DateTimeField()
    is_sent = models.BooleanField(default=False)
    
    
    def __str__(self) -> str:
        return self.notification_title
    

class OfferMail(models.Model):
    mail_subject = models.CharField(max_length=120)
    email = models.TextField()
    schedule_date = models.DateTimeField()
    is_sent = models.BooleanField(default=False)
    
    
    def __str__(self) -> str:
        return self.mail_subject
    
    

@receiver(post_save, sender=Order)
def order_status_handler(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    
    if not created:
        data = {}
        data['status'] = instance.order_status
        progres_percentage = 0
        
        if instance.order_status == 'order_receive':
            progres_percentage = 20
        
        if instance.order_status == 'breking':
            progres_percentage = 40
        
        if instance.order_status == 'breked':
            progres_percentage = 60
        
        if instance.order_status == 'out_of_delivery':
            progres_percentage = 80
            
        if instance.order_status == 'customar_receive':
            progres_percentage = 100
            
        
        data['progress'] = progres_percentage
        
        test = 'order_%s' % instance.order_id
        print('>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<')
        print(test)
      
        async_to_sync(channel_layer.group_send)(
            'order_%s' % instance.order_id,
            {
                'type':'order.status',
                'data':data
            }
        )
        
    
    
@receiver(post_save, sender=Notification)
def order_status_handler(sender, instance, created, **kwargs):
    if created:
        schedule, creat = CrontabSchedule.objects.get_or_create(
                            hour=instance.schedule_date.hour, 
                            minute=instance.schedule_date.minute, 
                            day_of_month=instance.schedule_date.day,
                            month_of_year=instance.schedule_date.month
                            )
        
        task = PeriodicTask.objects.create(crontab=schedule, name='notification-' + str(instance.id), task='food_delivery_app.task.SendNotification', args=[instance.id])