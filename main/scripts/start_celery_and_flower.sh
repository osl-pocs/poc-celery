#!/bin/bash

# Fetch the Redis IP address by directly invoking the get_redis_ip function
REDIS_IP=$(python -c 'from main.scripts.get_container_ip import get_redis_ip; print(get_redis_ip())')

# Validate the fetched IP
if [ -z "$REDIS_IP" ]; then
    echo "Failed to get Redis IP address."
    exit 1
fi

echo "Redis IP: $REDIS_IP"

# Start the Celery worker
echo "Starting Celery worker..."
celery -A main.celery_app worker --loglevel=INFO &

# Start Flower
echo "Starting Flower with Redis at $REDIS_IP..."
celery -A main.celery_app flower --broker=redis://$REDIS_IP:6379/0 &

echo "Celery and Flower have been started."
