#!/bin/bash

echo "Forcefully killing Celery and Flower processes..."

# Function to forcefully kill a process by its name
force_kill_process() {
    local process_name=$1
    echo "Searching for processes named $process_name to kill..."

    # Use pgrep to find all process IDs matching the process name and kill them
    pids=$(pgrep -f "$process_name")
    if [ ! -z "$pids" ]; then
        echo "Found processes with IDs: $pids. Force killing..."
        echo $pids | xargs kill -9
        echo "$process_name processes have been forcefully terminated."
    else
        echo "No $process_name processes found running."
    fi
}

# Specific names or part of the command that was used to start Celery and Flower
force_kill_process "celery -A src.poc_celery.celery_app worker"
force_kill_process "celery -A src.poc_celery.celery_app flower"

echo "All relevant Celery and Flower processes have been forcefully killed."
