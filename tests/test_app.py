import threading
import pytest

import requests
import time
from jason_server.derulo import run


def describe_endpoint():

    home_url = "http://127.0.0.1:8100"
    persons_url = "http://127.0.0.1:8100/persons"
    persons_url_page1 = "http://127.0.0.1:8100/persons?_page=1"
    persons_url_page2 = "http://127.0.0.1:8100/persons?_page=2"
    persons_url_page1_limit3 = "http://127.0.0.1:8100/persons?_page=1&_limit=3"
    persons_url_page2_limit3 = "http://127.0.0.1:8100/persons?_page=2&_limit=3"
    persons_url_page3_limit3 = "http://127.0.0.1:8100/persons?_page=3&_limit=3"
    persons_url_page4_limit3 = "http://127.0.0.1:8100/persons?_page=4&_limit=3"
    persons_url_page5_limit3 = "http://127.0.0.1:8100/persons?_page=5&_limit=3"

    @pytest.fixture()
    def s():
        # Wait for jason_server
        time.sleep(2)

        s = requests.Session()
        yield s

    def get(s):
        r = s.get(home_url)
        assert 200 == r.status_code

        r = s.get(persons_url)
        assert 200 == r.status_code
        assert 'application/json' == r.headers['content-type']
        data = r.json()
        assert 13 == len(data['data'])

    def get_with_paginate(s):
        r = s.get(persons_url_page1)
        assert 200 == r.status_code
        data = r.json()
        assert 10 == len(data['data'])

        r = s.get(persons_url_page2)
        assert 200 == r.status_code
        data = r.json()
        assert 3 == len(data['data'])

    def get_with_paginate_and_limit(s):
        r = s.get(persons_url_page1_limit3)
        assert 200 == r.status_code
        data = r.json()
        assert 3 == len(data['data'])

        r = s.get(persons_url_page2_limit3)
        assert 200 == r.status_code
        data = r.json()
        assert 3 == len(data['data'])

        r = s.get(persons_url_page3_limit3)
        assert 200 == r.status_code
        data = r.json()
        assert 3 == len(data['data'])

        r = s.get(persons_url_page4_limit3)
        assert 200 == r.status_code
        data = r.json()
        assert 3 == len(data['data'])

        r = s.get(persons_url_page5_limit3)
        assert 200 == r.status_code
        data = r.json()
        assert 1 == len(data['data'])
