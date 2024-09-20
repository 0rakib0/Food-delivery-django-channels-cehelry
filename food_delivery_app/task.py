from celery import shared_task
from time import sleep
import json
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
import asyncio
from channels.layers import get_channel_layer
from . import models
from celery.exceptions import Ignore


@shared_task(bind=True)
def Email_send(self, data):
    users = User.objects.all()
    email_info = json.loads(data[0])
    email_sub = email_info['email_sub']
    email_content = email_info['mail_content']
    sleep(10)
    for user in users:
        mail_sub = email_sub
        message = email_content
        to_mail = user.email
        send_mail  (
            subject = mail_sub,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_mail],
            fail_silently=True,
        )
    
    return "Task Compleated"

@shared_task(bind=True)
def SendNotification(self, id):
    try:
        notification = models.Notification.objects.filter(id=id).first()
        if notification:
            channel_layer = get_channel_layer()
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(channel_layer.group_send(
                    'notification_brotcast',
                    {
                        'type':'notifiction_send',
                        'data':'Hello Bangladesh'
                    }
                )
            )
            
        else:
            self.update_state(
                state = 'FAILURE',
                meta = {'exe': "Not Found"}
            )
            raise Ignore()
    except models.Notification.DoesNotExist:
            self.update_state(
                state = 'FAILURE',
                meta = {'exe': "Not Found"}
            )
            raise Ignore()