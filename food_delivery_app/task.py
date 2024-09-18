from celery import shared_task
from time import sleep


@shared_task()
def test_task(bind=True):
    for i in range(10):
        sleep(1)
        print(i)
    
    return "Task Compleated"