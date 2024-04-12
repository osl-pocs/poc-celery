# Celery with Subcollectors

## Overview

This proof of concept (PoC) demonstrates a distributed task queue implementation using Celery with Redis as the message broker. The project simulates a data collection and processing workflow using a system of subcollectors. Each subcollector generates a random list of integers for a given topic, and the results are aggregated, cleaned, and processed.

### Purpose

The primary goal of this PoC is to test and demonstrate the capability of Celery to manage complex workflows involving multiple asynchronous tasks. It showcases how to:

- Dispatch tasks to subcollectors in parallel.
- Aggregate results from all subcollectors.
- Perform cleanup and processing on aggregated data.

## Project Structure

- `celery_app.py`: Initializes the Celery app and includes the configuration for the Celery connection to Redis.
- `tasks.py`: Contains the definition of all Celery tasks, including subcollectors, data aggregation, cleanup, and processing tasks.
- `tests/`: Directory containing test files to validate the functionality of the Celery tasks.
  - `test_tasks.py`: Implements tests for each Celery task using pytest.
- `conda/base.yaml`: Conda environment file listing all necessary Python dependencies for the project.

## Workflow

The Celery workflow in this project orchestrates a series of tasks to simulate a data collection and processing pipeline using subcollector tasks. The workflow leverages Celery's capabilities for asynchronous task execution, task grouping, and result aggregation. Below is a step-by-step breakdown of the workflow:

### 1. Task Initiation with `collector_request`

- **Functionality**: The workflow begins with the `collector_request` task, which initiates the data collection process based on a specified topic.
- **Key Methods**:
  - `generate_collector_request(topic: str) -> str`: Generates a unique request ID for the collection request.
  - `group()`: Groups multiple subcollector tasks (`collector_1`, `collector_2`, `collector_3`) to be executed in parallel.
  - `chord(group())(callback)`: A `chord` is a Celery primitive that takes a group of tasks and a callback task. It ensures that the callback task (`collector_gathering`) is executed only after all tasks in the group have completed.

### 2. Parallel Execution of Subcollector Tasks

- **Subcollectors**: `collector_1`, `collector_2`, `collector_3`
- **Functionality**: Each subcollector task generates a random list of integers simulating the collection of data for the given topic.
- **Execution**: These tasks are executed in parallel as part of the `group` passed to the `chord`. This parallel execution is enabled by the `.apply_async()` method, ensuring that each task can run concurrently without waiting for the others.

### 3. Aggregation and Processing

- **Callback Task**: `collector_gathering`
  - **Functionality**: Aggregates the results from all subcollector tasks. This task acts as the callback for the `chord`, which means it automatically receives the aggregated results of the group as its input.
  - **Method Calls**:
    - `cleanup.delay(combined_result, request_id)`: After aggregation, the `cleanup` task is called asynchronously with the `.delay()` method, passing the combined results for further processing.
- **Cleanup Task**: `cleanup`
  - **Functionality**: Performs preliminary processing or cleanup on the aggregated data.
  - **Method Calls**:
    - `process.delay(data, request_id)`: Calls the `process` task asynchronously for final processing.
- **Process Task**: `process`
  - **Functionality**: Conducts the final processing of the data. In this example, it counts the total items and prints the result.
  - **Returns**: A dictionary with the `request_id` and the `item_count`, providing a simple summary of the processing outcome.

### Summary

This workflow demonstrates the power of Celery for handling complex asynchronous task pipelines. It showcases task parallelization (`group`), conditional task execution based on the completion of a group of tasks (`chord`), and chaining further processing steps (`delay`). Each task is designed to perform a specific role within the data collection and processing pipeline, from initiating collection requests to final data processing.

### Best Practices

- **Asynchronous Execution**: Utilize Celery's asynchronous task execution to enhance performance and scalability.
- **Task Chaining and Callbacks**: Leverage `chord` and `.delay()` for task chaining and callbacks, ensuring tasks are executed in the desired order and only after necessary prerequisites are met.
- **Error Handling**: Implement comprehensive error handling within tasks to manage failures gracefully and maintain workflow integrity.

## Setup Instructions

### Prerequisites

- Docker
- Conda or Mamba

### Environment Setup

1. Clone the repository and navigate to the project directory.

2. Create a new Conda environment using the `base.yaml` file:

   ```bash
   mamba env create -f conda/base.yaml
   ```

   Or, if you're using Conda:

   ```bash
   mamba env create -f conda/base.yaml
   ```

3. Activate the new environment:

   ```bash
   mamba activate celery-collectors
   ```

### Redis Setup Using Docker

Run a Redis container with the following command:

```bash
docker run --name redis -d redis redis-server --save 60 1 --loglevel warning
```

This command starts a Redis server in a Docker container named `redis`, with data saving configured and log level set to `warning`.

### Starting the Celery App

With the Redis server running and the environment activated, start the Celery worker:

```bash
celery -A main.celery_app worker --loglevel=info
```

This command initiates a Celery worker that listens for tasks as defined in `main.celery_app`.

### Running Tests

Ensure your Celery worker and Redis server are running, then execute the tests using pytest:

```bash
pytest tests/
```

This command runs all tests defined in the `tests/` directory, verifying the functionality of your Celery tasks.

## Conclusion

This PoC demonstrates a scalable and efficient way to manage distributed tasks using Celery with Redis as a message broker. It exemplifies a practical application of Celery's capabilities in handling complex workflows with multiple asynchronous tasks, showcasing a system that can be adapted for various data processing and aggregation needs.

