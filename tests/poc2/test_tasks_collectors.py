import unittest
from unittest.mock import patch, MagicMock
from poc_celery.poc2.tasks import (
    search_task,
    get_article,
    collector_1,
)  # Adjust the import path


class TestCeleryTasks(unittest.TestCase):
    @patch("poc_celery.poc2.tasks.Search.create")
    @patch("poc_celery.poc2.tasks.group")
    @patch("poc_celery.poc2.tasks.collector_1.s")
    @patch("poc_celery.poc2.tasks.collector_2.s")
    @patch("poc_celery.poc2.tasks.collector_3.s")
    @patch("poc_celery.poc2.tasks.clean_up.s")
    def test_search_task(
        self,
        mock_cleanup,
        mock_collector_3,
        mock_collector_2,
        mock_collector_1,
        mock_group,
        mock_create,
    ):
        # Mocking the Search.create() to return an object with an id attribute
        mock_search_obj = MagicMock()
        mock_search_obj.id = 1
        mock_create.return_value = mock_search_obj

        # Testing search_task
        search_task("test query")

        # Asserting Search.create was called with the right query
        mock_create.assert_called_once_with(query="test query")

        # Assert that collector tasks and cleanup tasks are setup correctly
        mock_collector_1.assert_called_once_with(1)
        mock_collector_2.assert_called_once_with(1)
        mock_collector_3.assert_called_once_with(1)
        mock_cleanup.assert_called_once_with(search_id=1)
        mock_group.assert_called_once()

    @patch("poc_celery.poc2.tasks.Article.objects.create")
    def test_get_article(self, mock_create):
        # Test get_article task
        get_article(1, 101, "collector_1")

        # Asserting Article.create was called with correct parameters
        mock_create.assert_called_once_with(
            search_id=1, meta="Metadata for article 101 from collector_1"
        )


if __name__ == "__main__":
    unittest.main()
