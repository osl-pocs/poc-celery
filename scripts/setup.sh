#!/usr/bin/env bash

set -ex

docker run --rm --name rabbitmq -d -p 5672:5672 rabbitmq || true
docker run --rm --name redis -d -p 6379:6379 redis || true
bash scripts/start_celery_and_flower.sh &
