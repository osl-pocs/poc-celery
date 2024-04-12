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

## Monitoring Celery Tasks with Flower

### Using the Startup Script

To facilitate an efficient development and monitoring environment, we've prepared a bash script `start_celery_and_flower.sh` that simultaneously starts a Celery worker and Flower, a real-time monitoring tool. This script fetches the Redis container's IP address dynamically, ensuring that both Celery and Flower are correctly configured to communicate with Redis as the broker.

To start both the Celery worker and Flower, navigate to your project's root directory and run:

```bash
bash main/scripts/start_celery_and_flower.sh
```

This command executes the script that:

1. **Starts a Celery Worker**: Launches a Celery worker instance using `main.celery_app` as the application module. This worker listens for tasks dispatched to the queues and executes them as they arrive.
   
2. **Launches Flower**: Initiates Flower on the default port (5555), allowing you to access a web-based user interface to monitor and manage the Celery worker and tasks. Flower provides insights into task progress, worker status, task history, and much more, making it an invaluable tool for debugging and optimizing your task workflows.


### Executing the Tests with Pytest

With your environment prepared and the celery launched, you can now run the tests using pytest. Navigate to the root directory of your project and execute:

```bash
pytest -vvv tests/
```

- **Interpreting Results**: Pytest will provide a summary indicating which tests passed, failed, or were skipped. For any failures, detailed error information and traceback will be provided to aid in debugging.

## Best Practices in Asynchronous Task Management with Celery and Flower

### Embracing Celery's Asynchronous Capabilities

In this project, we harness Celery's powerful asynchronous task execution to bolster performance and scalability. Here are some key best practices we've applied:

- **Decoupling Components**: By employing Celery, we effectively decouple the task execution from the main application flow. This separation allows for more scalable and maintainable code architecture.

- **Optimizing Task Execution**: Utilizing Celery's `group`, `chain`, and `chord` primitives, we've structured complex task workflows that maximize concurrency and minimize processing time. This structured approach ensures tasks are executed in an optimal sequence and only after all required dependencies have been satisfied.

- **Robust Error Handling**: We've implemented strategic error handling within our tasks to ensure resilience. By catching exceptions and using retry mechanisms where applicable, we maintain the integrity of our task pipeline, even in the face of transient failures.

### Leveraging Flower for Enhanced Task Monitoring and Management

Flower is a critical tool for our project, providing comprehensive monitoring and management capabilities for our Celery workers and tasks. Here's why Flower is indispensable:

- **Visibility**: Flower's real-time monitoring gives us instant visibility into our task queues, worker status, and the progress of task execution. This level of insight is invaluable for quickly identifying bottlenecks or failures in the task pipeline.

- **Direct Task Management**: Through Flower's web interface, we gain direct control over task execution. The ability to cancel tasks, restart workers, and adjust task priorities on-the-fly empowers us to maintain optimal task flow under varying load conditions.

- **Insights for Debugging and Optimization**: Flower's detailed execution statistics for each task guide our debugging and optimization efforts. Analyzing task durations, success rates, and retry counts helps us pinpoint inefficiencies and improve the overall performance of our task workflows.

- **Remote Accessibility**: The web-based interface of Flower means we can monitor and manage our task environment from any location, facilitating remote debugging and administration without the need for direct server access.

### Additional Practices

- **Environment Isolation**: Utilizing virtual environments and containerization (e.g., Docker) for our Celery and Redis setup ensures consistency across development, testing, and production environments, reducing the "it works on my machine" syndrome.

- **Automated Testing**: Our project includes a suite of automated tests to validate task logic, asynchronous behavior, and failure handling scenarios. These tests, integrated into a CI/CD pipeline, ensure code quality and prevent regressions.

- **Documentation and Logging**: Comprehensive documentation, including clear docstrings and READMEs, alongside detailed logging within tasks, facilitates easier maintenance and accelerates the onboarding process for new developers.

## Conclusion

This PoC demonstrates a scalable and efficient way to manage distributed tasks using Celery with Redis as a message broker. It exemplifies a practical application of Celery's capabilities in handling complex workflows with multiple asynchronous tasks, showcasing a system that can be adapted for various data processing and aggregation needs.
