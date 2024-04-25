from __future__ import annotations

from celery import group, shared_task

from poc_celery.db import Article, Search, SimpleORM

SimpleORM.setup()


@shared_task
def search_task(query: str):
    """
    Start the pipeline.

    Initial task that receives a user's request and triggers collector tasks.
    """
    # with transaction.atomic():
    search_obj = Search.create(query=query)
    search_id = search_obj.id

    collectors = [
        collector_1.s(search_id),
        collector_2.s(search_id),
        collector_3.s(search_id),
    ]
    callback = clean_up.s(search_id=search_id).set(
        link_error=clean_up.s(search_id=search_id)
    )
    group(collectors) | callback.delay()


@shared_task(bind=True, max_retries=0)
def collector_1(self, search_id: int):
    """Collect data for collector 1."""
    return execute_collector_tasks(search_id, "collector_1")


@shared_task(bind=True, max_retries=0)
def collector_2(self, search_id: int):
    """Collect data for collector 2."""
    return execute_collector_tasks(search_id, "collector_2")


@shared_task(bind=True, max_retries=0)
def collector_3(self, search_id: int):
    """Collect data for collector 3."""
    return execute_collector_tasks(search_id, "collector_3")


def execute_collector_tasks(search_id: int, collector_name: str):
    """
    Execute collector tasks.

    Helper function to execute get_list and get_article tasks for a collector.
    """
    # Assuming `get_list` generates a list of article IDs for simplicity
    article_ids = get_list(search_id, collector_name)
    for article_id in article_ids:
        get_article.delay(search_id, article_id, collector_name)
    return {"status": "Completed", "collector": collector_name}


@shared_task
def get_list(search_id: int, collector_name: str):
    """Simulated task to get a list of articles."""
    # Simulate getting a list of article IDs
    return [1, 2, 3]  # Example article IDs


@shared_task
def get_article(search_id: int, article_id: int, collector_name: str):
    """Task to fetch and save article metadata."""
    # Simulate fetching article metadata
    metadata = f"Metadata for article {article_id} from {collector_name}"
    # with transaction.atomic():
    Article.objects.create(search_id=search_id, meta=metadata)


@shared_task
def clean_up(search_id: int):
    """
    Clean up temporary storage.

    Cleanup task to be triggered when all articles from all collectors
    for a specific search are done.
    """
    # Implement cleanup logic here, e.g., removing duplicate articles
    pass
