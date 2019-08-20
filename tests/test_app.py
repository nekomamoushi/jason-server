import threading
import pytest

import requests
import time
from jason_server.derulo import run

@pytest.fixture(autouse=True)
def json_server():

    options = {
        'host': 'localhost',
        'port': 8100
    }
    database = 'tests/data/sample_database.json'
    thread = threading.Thread(
        target=run,
        args=(options, database),
        daemon=True
    )
    thread.start()
    yield


def test_app(json_server):
    home_url = "http://127.0.0.1:8100"
    articles_url = "http://127.0.0.1:8100/articles"
    authors_url = "http://127.0.0.1:8100/authors"

    # Wait for jason_server
    time.sleep(2)

    s = requests.Session()

    r = s.get(home_url)
    assert 200 == r.status_code

    r = s.get(articles_url)
    assert 200 == r.status_code
    assert 'application/json' == r.headers['content-type']
    data = r.json()
    assert 2 == len(data['data'])

    r = s.get(authors_url)
    assert 200 == r.status_code
    assert 'application/json' == r.headers['content-type']
    data = r.json()
    assert 3 == len(data['data'])


