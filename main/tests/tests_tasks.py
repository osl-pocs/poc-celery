import pytest
from main.celery_app import app
from main.tasks import collector_request, generate_collector_request
from unittest.mock import patch
from main.celery_app import REDIS_IP
import logging

# Configure logging for visibility during test runs
logging.basicConfig(level=logging.INFO)

@pytest.fixture(scope='module')
def celery_config():
    """
    Configure Celery for testing purposes.
    
    Returns
    -------
    dict
        A dictionary with configuration settings for the Celery app, including the broker URL,
        result backend, and a flag to execute tasks eagerly.
    """
    return {
        'broker_url': f'redis://{REDIS_IP}:6379/0',
        'result_backend': 'db+sqlite:///test_results.sqlite',
        'task_always_eager': True,  # Execute tasks immediately rather than sending to the queue
    }

@pytest.fixture(scope='module')
def celery_enable_logging():
    """
    Enable logging for Celery tasks during testing.
    
    Returns
    -------
    bool
        A flag indicating whether to enable logging.
    """
    return True

@pytest.fixture(autouse=True)
def setup_test_environment():
    """
    Setup and teardown for the test environment.
    
    Yields
    ------
    None
    """
    # Setup code here, if necessary (e.g., mocking database connections)
    yield
    # Teardown code here, if necessary

def test_generate_collector_request():
    """
    Test the generate_collector_request function to ensure it generates a valid UUID.
    
    Parameters
    ----------
    None
    
    Assertions
    ----------
    Asserts that the returned request_id is a string.
    """
    topic = "test_topicA"
    request_id = generate_collector_request(topic)
    assert isinstance(request_id, str), "The request_id should be a string."

def test_collector_request_triggers_sub_collectors():
    """
    Test that the collector_request task correctly triggers the sub collector tasks.
    
    This test assumes that the sub collector tasks (collector_1, collector_2, and collector_3)
    eventually do something observable, like writing to a database or emitting a log.
    For simplicity, the test checks if the function itself was called, without using `.s` or `apply_async`.
    
    Parameters
    ----------
    None
    
    Assertions
    ----------
    Asserts that each sub collector task was called once.
    """
    topic = "test_topic"
    
    with patch('main.tasks.collector_1') as mock_collector_1, \
         patch('main.tasks.collector_2') as mock_collector_2, \
         patch('main.tasks.collector_3') as mock_collector_3:
        
        collector_request(topic)
        
        mock_collector_1.assert_called_once()
        mock_collector_2.assert_called_once()
        mock_collector_3.assert_called_once()
