from celery import shared_task
from time import sleep
import json

@shared_task(bind=True)
def Email_send(self, data):
    print("-----------____________---------")
    email_info = json.loads(data[0])
    email_sub = email_info['email_sub']
    email_content = email_info['mail_content']
    
    print(email_sub)
    print(email_content)
    
    return "Task Compleated"