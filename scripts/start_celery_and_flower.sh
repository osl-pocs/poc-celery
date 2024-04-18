#!/bin/bash

# Fetch the Rabbitmq IP address by directly invoking the get_amqp_ip function
AMQP_IP=$(python -c 'from main.get_container_ip import get_amqp_ip; print(get_amqp_ip())')

# Validate the fetched IP
if [ -z "$AMQP_IP" ]; then
    echo "Failed to get Rabbitmq IP address."
    exit 1
fi

echo "Rabbitmq IP: $AMQP_IP"

# Start the Celery worker
echo "Starting Celery worker..."
celery -A main.celery_app worker --loglevel=INFO &

# Start Flower
echo "Starting Flower with Rabbitmq at $AMQP_IP..."
celery -A main.celery_app flower --broker=amqp://guest:guest@{AMQP_IP}:5672 &

echo "Celery and Flower have been started."
