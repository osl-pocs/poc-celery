import pytest


@pytest.fixture(scope="module")
def celery_config():
    """
    Provide Celery app configuration for testing.

    This fixture is responsible for setting up the Celery app with a specific
    configuration suitable for test runs. It defines the broker and result backend
    to use Rabbitmq and sets the task execution mode to always eager, which means
    tasks will be executed locally and synchronously.

    Yields
    ------
    dict
        A dictionary containing configuration settings for the Celery application.
    """
    return {
        "broker_url": "amqp://guest:guest@rabbitmq3:5672",
        "result_backend": "redis://localhost:6379/0",
        "task_always_eager": True,
    }


@pytest.fixture(scope="module")
def celery_enable_logging():
    """
    Activate logging for Celery tasks during testing.

    This fixture ensures that Celery task logs are visible during test execution,
    aiding in debugging and verifying task behavior.

    Returns
    -------
    bool
        True to enable Celery task logging, False otherwise.
    """
    return True
