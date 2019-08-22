import pytest

import requests
import time

URL_HOME = "http://127.0.0.1:8100"
URL_PERSONS = "http://127.0.0.1:8100/persons"

URL_PERSONS_FILTER_AGE_30 = "http://127.0.0.1:8100/persons?age=30"
URL_PERSONS_FILTER_AGE_30_MALE = "http://127.0.0.1:8100/persons?age=30&gender=male"
URL_PERSONS_FILTER_AGE_30_FEMALE = "http://127.0.0.1:8100/persons?age=30&gender=female"

URL_PERSONS_PAGE_1 = "http://127.0.0.1:8100/persons?_page=1"
URL_PERSONS_PAGE_2 = "http://127.0.0.1:8100/persons?_page=2"

URL_PERSONS_PAGE_1_LIMIT_3 = "http://127.0.0.1:8100/persons?_page=1&_limit=3"
URL_PERSONS_PAGE_2_LIMIT_3 = "http://127.0.0.1:8100/persons?_page=2&_limit=3"
URL_PERSONS_PAGE_3_LIMIT_3 = "http://127.0.0.1:8100/persons?_page=3&_limit=3"
URL_PERSONS_PAGE_4_LIMIT_3 = "http://127.0.0.1:8100/persons?_page=4&_limit=3"
URL_PERSONS_PAGE_5_LIMIT_3 = "http://127.0.0.1:8100/persons?_page=5&_limit=3"

URL_PERSONS_SORT_BY_AGE = "http://127.0.0.1:8100/persons?_sort=age"
URL_PERSONS_SORT_BY_NAME = "http://127.0.0.1:8100/persons?_sort=name"

URL_PERSONS_SORT_BY_AGE_PAGE_1 = "http://127.0.0.1:8100/persons?_sort=age&_page=1"
URL_PERSONS_SORT_BY_NAME_PAGE_2 = "http://127.0.0.1:8100/persons?_sort=name&_page=2"
URL_PERSONS_SORT_DESC_BY_AGE_PAGE_1 = "http://127.0.0.1:8100/persons?_sort=age&_order=desc&_page=1"
URL_PERSONS_SORT_BY_NAME_PAGE_2_LIMIT_4 = "http://127.0.0.1:8100/persons?_sort=name&_page=2&_limit=4"


def describe_endpoint():

    @pytest.fixture()
    def s():
        # Wait for jason_server
        time.sleep(1)

        s = requests.Session()
        yield s

    def get(s):

        r = s.get(URL_HOME)
        assert 200 == r.status_code

        r = s.get(URL_PERSONS)
        assert 200 == r.status_code
        assert 'application/json' == r.headers['content-type']
        data = r.json()
        assert 13 == len(data['data'])

    def get_with_filter(s):

        r = s.get(URL_PERSONS_FILTER_AGE_30)
        assert 200 == r.status_code
        data = r.json()
        assert 3 == len(data['data'])

        r = s.get(URL_PERSONS_FILTER_AGE_30_MALE)
        assert 200 == r.status_code
        data = r.json()
        assert 2 == len(data['data'])

        r = s.get(URL_PERSONS_FILTER_AGE_30_FEMALE)
        assert 200 == r.status_code
        data = r.json()
        assert 1 == len(data['data'])

    def get_with_paginate(s):

        r = s.get(URL_PERSONS_PAGE_1)
        assert 200 == r.status_code
        data = r.json()
        assert 10 == len(data['data'])

        r = s.get(URL_PERSONS_PAGE_2)
        assert 200 == r.status_code
        data = r.json()
        assert 3 == len(data['data'])

    def get_with_paginate_and_limit(s):

        r = s.get(URL_PERSONS_PAGE_1_LIMIT_3)
        assert 200 == r.status_code
        data = r.json()
        assert 3 == len(data['data'])

        r = s.get(URL_PERSONS_PAGE_2_LIMIT_3)
        assert 200 == r.status_code
        data = r.json()
        assert 3 == len(data['data'])

        r = s.get(URL_PERSONS_PAGE_3_LIMIT_3)
        assert 200 == r.status_code
        data = r.json()
        assert 3 == len(data['data'])

        r = s.get(URL_PERSONS_PAGE_4_LIMIT_3)
        assert 200 == r.status_code
        data = r.json()
        assert 3 == len(data['data'])

        r = s.get(URL_PERSONS_PAGE_5_LIMIT_3)
        assert 200 == r.status_code
        data = r.json()
        assert 1 == len(data['data'])

    def get_with_sorting(s):

        r = s.get(URL_PERSONS_SORT_BY_AGE)
        assert 200 == r.status_code
        data = r.json()
        assert 21 == data['data'][0]['age']
        assert "Bell Hinton" == data['data'][0]['name']

        r = s.get(URL_PERSONS_SORT_BY_NAME)
        assert 200 == r.status_code
        data = r.json()
        assert 30 == data['data'][0]['age']
        assert "Anastasia Coffey" == data['data'][0]['name']

    def get_with_sorting_and_pagination(s):

        r = s.get(URL_PERSONS_SORT_BY_AGE_PAGE_1)
        assert 200 == r.status_code
        data = r.json()
        assert 23 == data['data'][1]['age']

        r = s.get(URL_PERSONS_SORT_BY_NAME_PAGE_2)
        assert 200 == r.status_code
        data = r.json()
        assert 36 == data['data'][1]['age']

        r = s.get(URL_PERSONS_SORT_DESC_BY_AGE_PAGE_1)
        assert 200 == r.status_code
        data = r.json()
        assert 37 == data['data'][1]['age']

        r = s.get(URL_PERSONS_SORT_BY_NAME_PAGE_2_LIMIT_4)
        assert 200 == r.status_code
        data = r.json()
        assert 23 == data['data'][0]['age']
