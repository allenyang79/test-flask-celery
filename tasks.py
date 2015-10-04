from celery import Celery
import time

REDIS_HOST = "192.168.99.100"
celery = Celery('tasks', 
    backend='redis://{}'.format(REDIS_HOST), 
    broker='redis://{}'.format(REDIS_HOST) 
)

@celery.task
def add(x, y):
    for i in range(0,x+y):
        time.sleep(0.1)
        print "sleep...",i
    return x + y
