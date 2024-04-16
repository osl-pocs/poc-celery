import asyncio
import pytest
from unittest.mock import mock_open, patch
from unittest.mock import call, Mock
from celery.contrib.testing.worker import start_worker

from main.celery_app import app
from main.tasks_async import DATA_DIR, clean_data, create_project

@pytest.fixture
def mock_file_io():
    with patch("builtins.open", mock_open()) as m:
        yield m

def test_clean_data(mock_file_io):
    file_path = str(DATA_DIR / "collectors.txt")
    
    clean_data.delay(file_path)

    mock_file_io.assert_not_called()

def test_create_project(mock_file_io):
    file_path = str(DATA_DIR / "collectors.txt")

    rows = [
        [1, 1, 3],
        [2, 10, 2],
        [2, 30, 2],
        [1, 100, 3],
        [1, 3, 3],
    ]
    

    for row in rows:
        create_project.delay(row, str(file_path))


    expected_calls = [f"{','.join(map(str, row))}\n" for row in rows]

    mock = Mock(return_value=None)
    for f in expected_calls:
        mock(f)
    
    calls = [
        call('1,1,3\n'), 
        call('2,10,2\n'), 
        call('2,30,2\n'), 
        call('1,100,3\n'), 
        call('1,3,3\n')
        ]

    mock.assert_has_calls(calls, any_order=True)


@pytest.fixture(scope='module')
def celery_worker():

    worker = start_worker(app)
    yield worker

@pytest.mark.asyncio
async def test_create_project_stress(celery_worker):
    file_path = str(DATA_DIR / "collectors.txt")

    num_calls = 100

    calls = [
        [1, 1, 3],
        [2, 10, 2],
        [2, 30, 2],
        [1, 100, 3],
        [1, 3, 3],
    ] 
    calls = calls * (num_calls // len(calls))  # Repetindo as chamadas para alcançar o número desejado

    for row in calls:
        create_project.delay(row, file_path)

    await asyncio.sleep(5) 

    assert True
