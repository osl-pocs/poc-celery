import random
import uuid
from celery import chord
from main.celery_app import app

def generate_collector_request(topic: str) -> str:
    """
    Generates a unique identifier for a collector request.

    Parameters
    ----------
    topic : str
        The topic for which the request is being made.

    Returns
    -------
    str
        A unique identifier for the request.
    """
    return str(uuid.uuid4())

@app.task
def collector_request(topic: str):
    """
    Initiates collection requests by dispatching tasks to subcollectors.

    Parameters
    ----------
    topic : str
        The topic for which the collection is requested.
    """
    request_id = generate_collector_request(topic)
    results = [collector_1(topic, request_id), collector_2(topic, request_id), collector_3(topic, request_id)]
    collector_gathering(request_id, results)

@app.task
def collector_1(topic: str, request_id: str) -> list:
    """
    Simulates a subcollector task for a given topic, generating a random list.

    Parameters
    ----------
    topic : str
        The topic for which the collection is being made.
    request_id : str
        The unique identifier for the collection request.

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

    Parameters
    ----------
    topic : str
        The topic for which the collection is being made.
    request_id : str
        The unique identifier for the collection request.
    """
    random_list = [random.randint(0, 100) for _ in range(random.randint(0, 10))]
    collector_gathering.s(random_list, request_id).apply_async()

@app.task
def collector_3(topic: str, request_id: str) -> None:
    """
    Processes the third subcollector task.

    Parameters
    ----------
    topic : str
        The topic for which the collection is being made.
    request_id : str
        The unique identifier for the collection request.
    """
    random_list = [random.randint(0, 100) for _ in range(random.randint(0, 10))]
    collector_gathering.s(random_list, request_id).apply_async()

@app.task
def collector_gathering(request_id: str, results: list):
    """
    Aggregates results from all subcollectors and initiates the cleanup process.

    Parameters
    ----------
    request_id : str
        The unique identifier for the collection request.
    results : list
        A list containing the results from each subcollector.
    """
    combined_result = [item for sublist in results for item in sublist]
    cleanup(combined_result, request_id)

@app.task
def cleanup(data: list, request_id: str):
    """
    Performs cleanup operations on the collected data and proceeds to processing.

    Parameters
    ----------
    data : list
        The aggregated data from all subcollectors.
    request_id : str
        The unique identifier for the collection request.
    """
    print(f"Cleanup: {request_id}, Size: {len(data)}")
    process(data, request_id)

@app.task
def process(data: list, request_id: str):
    """
    Processes the cleaned data, providing final output.

    Parameters
    ----------
    data : list
        The cleaned and aggregated data from all subcollectors.
    request_id : str
        The unique identifier for the collection request.
    """
    item_count = len(data)
    print(f"Process: {request_id}, Total Items: {item_count}")
    return {'request_id': request_id, 'item_count': item_count}
