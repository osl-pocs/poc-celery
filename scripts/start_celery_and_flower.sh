#!/bin/bash

# Function to wait for a service to be available on a specific port
wait_for_service() {
    local host=$1
    local port=$2
    local timeout=$3

    echo "Waiting for service on $host:$port..."
    for ((i=0; i<timeout; i++)); do
        if nc -z $host $port > /dev/null 2>&1; then
            echo "Service on $host:$port is available."
            return 0
        fi
        sleep 1
    done
    echo "Timed out waiting for service on $host:$port."
    exit 1
}

# Check for required commands
command -v nc >/dev/null 2>&1 || { echo >&2 "This script requires 'nc' but it's not installed. Aborting."; exit 1; }

# Get RabbitMQ IP from a Python utility, assuming the function is reliable and necessary
AMQP_IP=$(python -c 'from src.poc_celery.get_container_ip import get_amqp_ip; print(get_amqp_ip())')

# Validate the fetched IP
if [[ -z "$AMQP_IP" ]]; then
    echo "Failed to get RabbitMQ IP address."
    exit 1
fi

# Wait for RabbitMQ to be fully operational
wait_for_service $AMQP_IP 5672 60

# Start Celery and Flower using the RabbitMQ IP
echo "Starting Celery worker..."
celery -A src.poc_celery.celery_app worker --loglevel=INFO &

echo "Starting Flower for monitoring Celery..."
celery -A src.poc_celery.celery_app flower &

echo "Celery and Flower dashboard have been started."
