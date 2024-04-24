from celery import Celery

from poc_celery.get_container_ip import get_amqp_ip, get_redis_ip

# Get the Rabbitmq container IP address
AMQP_IP = get_amqp_ip()
REDIS_IP = get_redis_ip()

# Create a Celery instance with Rabbitmq as the broker and result backend
app = Celery(
    "poc-celery",
    broker=f"amqp://guest:guest@{AMQP_IP}:5672",
    backend=f"redis://{REDIS_IP}:6379/0",
    include=[
        "poc_celery.poc1.tasks_async",
        "poc_celery.poc1.tasks_collectors",
    ],
)

# Set broker_connection_retry_on_startup to True to suppress the warning
app.conf.broker_connection_retry_on_startup = True

app.autodiscover_tasks()
