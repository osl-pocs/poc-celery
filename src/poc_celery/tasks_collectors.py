import random
import uuid

from celery import chord, group

from poc_celery.celery_app import app


def generate_collector_request(topic: str) -> str:
    """
    Generate a unique identifier for a collector request.

    Parameters
    ----------
    topic : str
        The topic name for which the collector request is being generated.

    Returns
    -------
    str
        A unique identifier (UUID4) for the collector request.
    """
    return str(uuid.uuid4())


@app.task
def collector_request(topic: str):
    """
    Generate a unique identifier for a collector request.

    Initiates the collection request by dispatching tasks to subcollectors
    and processes the aggregated results asynchronously using a chord.

    Parameters
    ----------
    topic : str
        The topic for which the collection is requested.
    """
    request_id = generate_collector_request(topic)
    callback = collector_gathering.s(request_id)
    chord_tasks = group(
        collector_1.s(topic, request_id),
        collector_2.s(topic, request_id),
        collector_3.s(topic, request_id),
    )
    chord(chord_tasks)(callback)


@app.task
def collector_1(topic: str, request_id: str) -> list:
    """
    Generate a random list of integers for the given topic.

    A subcollector task that generates a random list of integers.

    Parameters
    ----------
    topic : str
        The topic for which data is being collected.
    request_id : str
        A unique identifier for the collection request.

    Returns
    -------
    list
        A list of random integers.
    """
    return [random.randint(0, 100) for _ in range(random.randint(0, 10))]


@app.task
def collector_2(topic: str, request_id: str) -> None:
    """
    Processes the second subcollector task.

    A subcollector task that generates a random list of integers.

    Parameters
    ----------
    topic : str
        The topic for which data is being collected.
    request_id : str
        A unique identifier for the collection request.

    Returns
    -------
    list
        A list of random integers.
    """
    random_list = [
        random.randint(0, 100) for _ in range(random.randint(0, 10))
    ]
    collector_gathering.s(random_list, request_id).apply_async()


@app.task
def collector_3(topic: str, request_id: str) -> None:
    """
    Processes the third subcollector task.

    A subcollector task that generates a random list of integers.

    Parameters
    ----------
    topic : str
        The topic for which data is being collected.
    request_id : str
        A unique identifier for the collection request.

    Returns
    -------
    list
        A list of random integers.
    """
    random_list = [
        random.randint(0, 100) for _ in range(random.randint(0, 10))
    ]
    collector_gathering.s(random_list, request_id).apply_async()


@app.task
def collector_gathering(request_id: str, results: list):
    """
    Join the process for collectors.

    Aggregate the results from all subcollectors and proceeds with the cleanup
    process.

    This task is intended to be used as a callback for a group of subcollector
    tasks.

    Parameters
    ----------
    request_id : str
        A unique identifier for the collection request.
    results : list
        Aggregated results from all subcollector tasks.

    """
    combined_result = [item for sublist in results for item in sublist]
    cleanup.delay(combined_result, request_id)


@app.task
def cleanup(data: list, request_id: str):
    """
    Perform cleanup operations on the aggregated data from subcollectors.

    Parameters
    ----------
    data : list
        The aggregated data that needs to be cleaned.
    request_id : str
        A unique identifier for the collection request.
    """
    print(f"Cleanup: {request_id}, Size: {len(data)}")
    process.delay(data, request_id)


@app.task
def process(data: list, request_id: str):
    """
    Processes the cleaned data.

    Typically involving further analysis or storage.

    Parameters
    ----------
    data : list
        The cleaned data ready for processing.
    request_id : str
        A unique identifier for the collection request.

    Returns
    -------
    dict
        A dictionary containing the request_id and the total item count.
    """
    item_count = len(data)
    print(f"Process: {request_id}, Total Items: {item_count}")
    return {"request_id": request_id, "item_count": item_count}
