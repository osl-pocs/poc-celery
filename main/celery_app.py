
from celery import Celery

from main.scripts.get_container_ip import get_redis_ip

# Get the Redis container IP address
REDIS_IP = get_redis_ip()

# Create a Celery instance with Redis as the broker and result backend
app = Celery('celery-collectors', broker=f'redis://{REDIS_IP}:6379/0', backend=f'redis://{REDIS_IP}:6379/0',  include=["main.tasks"])

# Set broker_connection_retry_on_startup to True to suppress the warning
app.conf.broker_connection_retry_on_startup = True

app.autodiscover_tasks()
