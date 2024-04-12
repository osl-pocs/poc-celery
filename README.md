Below is a detailed and instructive `README.md` for your proof of concept (PoC) project using Celery with subcollectors, Redis, and Docker. This README includes sections on the project structure, workflow, purpose, and setup instructions.

---

# PoC Celery with Subcollectors

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

1. **Collector Request**: The workflow begins with a `collector_request` task that takes a topic as input and dispatches tasks to subcollectors (`collector_1`, `collector_2`, `collector_3`) in parallel.
2. **Subcollectors**: Each subcollector generates a random list of integers based on the given topic and sends its results to the `collector_gathering` task.
3. **Data Aggregation**: The `collector_gathering` task aggregates the results from all subcollectors.
4. **Cleanup**: The aggregated data is sent to the `cleanup` task, which performs any necessary data cleanup operations.
5. **Processing**: Finally, the cleaned data is processed by the `process` task, which counts the total items and completes the workflow.

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
   mamba activate poc-celery
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

