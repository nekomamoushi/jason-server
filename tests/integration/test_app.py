import pytest

import requests
import time


def describe_endpoint():

    @pytest.fixture()
    def s():
        # Wait for jason_server
        time.sleep(2)

        s = requests.Session()
        yield s

    def get(s):
        home_url = "http://127.0.0.1:8100"
        persons_url = "http://127.0.0.1:8100/persons"

        r = s.get(home_url)
        assert 200 == r.status_code

        r = s.get(persons_url)
        assert 200 == r.status_code
        assert 'application/json' == r.headers['content-type']
        data = r.json()
        assert 13 == len(data['data'])

    def get_with_paginate(s):
        persons_url_page1 = "http://127.0.0.1:8100/persons?_page=1"
        persons_url_page2 = "http://127.0.0.1:8100/persons?_page=2"

        r = s.get(persons_url_page1)
        assert 200 == r.status_code
        data = r.json()
        assert 10 == len(data['data'])

        r = s.get(persons_url_page2)
        assert 200 == r.status_code
        data = r.json()
        assert 3 == len(data['data'])

    def get_with_paginate_and_limit(s):
        persons_url_page1_limit3 = "http://127.0.0.1:8100/persons?_page=1&_limit=3"
        persons_url_page2_limit3 = "http://127.0.0.1:8100/persons?_page=2&_limit=3"
        persons_url_page3_limit3 = "http://127.0.0.1:8100/persons?_page=3&_limit=3"
        persons_url_page4_limit3 = "http://127.0.0.1:8100/persons?_page=4&_limit=3"
        persons_url_page5_limit3 = "http://127.0.0.1:8100/persons?_page=5&_limit=3"

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

    def get_with_sorting(s):
        persons_url_sort_by_age = "http://127.0.0.1:8100/persons?_sort=age"
        persons_url_sort_by_name = "http://127.0.0.1:8100/persons?_sort=name"

        r = s.get(persons_url_sort_by_age)
        assert 200 == r.status_code
        data = r.json()
        assert 21 ==data['data'][0]['age']
        assert "Bell Hinton" == data['data'][0]['name']

        r = s.get(persons_url_sort_by_name)
        assert 200 == r.status_code
        data = r.json()
        assert 30 == data['data'][0]['age']
        assert "Anastasia Coffey" == data['data'][0]['name']
