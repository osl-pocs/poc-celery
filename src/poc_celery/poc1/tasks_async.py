from pathlib import Path

from poc_celery.poc1.celery_app import app

# app = Celery('tasks', broker='your_broker_url', backend='your_backend_url')
DATA_DIR = Path(__file__).parent.parent / "data"


@app.task
def clean_data(file_path):
    """Cleans the data by clearing the collectors.txt file."""
    # Writing to file
    with open(file_path, "w") as f:
        f.write("")


@app.task
def create_project(row: list, file_path):
    """Appends a row of data to the collectors.txt file."""
    with open(DATA_DIR / "collectors.txt", "a") as f:
        text = ",".join([str(r) for r in row])
        f.write(f"{text}\n")
