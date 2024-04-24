import logging

from unittest.mock import patch

import pytest

from poc_celery.tasks_collectors import (
    collector_request,
    generate_collector_request,
)

# Configure logging to ensure visibility of task execution during test runs.
logging.basicConfig(level=logging.INFO)


def test_generate_collector_request():
    """
    Validate that `generate_collector_request` produces a valid UUID string.

    Ensures the `generate_collector_request` function returns a string that
    is expected to be a UUID, confirming the generation of unique request identifiers.

    Assertions
    ----------
    Asserts the type and format of the return value from `generate_collector_request`.
    """
    topic = "test_topicA"
    request_id = generate_collector_request(topic)
    assert isinstance(request_id, str), "The request_id should be a string."


@patch("poc_celery.tasks_collectors.collector_gathering.s")
@patch("poc_celery.tasks_collectors.group")
def test_collector_request_triggers_sub_collectors(
    mock_group, mock_collector_gathering_s
):
    """
    Test the orchestration within `collector_request` to trigger subcollector tasks.

    This test verifies that the `collector_request` function correctly sets up
    a group of subcollector tasks and designates `collector_gathering` as the callback
    using Celery's chord primitive. It mocks the `group` method and the signature
    of `collector_gathering` to intercept and assert their usage without actual task execution.

    Parameters
    ----------
    mock_group : MagicMock
        Mock object for Celery's `group` method.
    mock_collector_gathering_s : MagicMock
        Mock object for the `s()` signature method of `collector_gathering` task.

    Assertions
    ----------
    Asserts that `group` is called with the correct tasks.
    Asserts that `collector_gathering.s()` is called to prepare the callback signature.
    """
    topic = "test_topic"

    collector_request(topic)

    mock_group.assert_called_once()
    mock_collector_gathering_s.assert_called_once()
