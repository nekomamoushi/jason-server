
import pytest
from webtest import TestApp

from jason_server.derulo import app, create_database


BIG_DATABASE = "tests/data/big_database.json"


def test_sample_database():

    create_database(BIG_DATABASE)

    client = TestApp(app)

    r = client.get('/')
    assert 200 == r.status_code
    assert "http://localhost:8080/persons" in r.body.decode("utf-8")

    r = client.get('/db')
    assert 200 == r.status_code

    # Test singular route
    r = client.get('/persons')
    assert 200 == r.status_code
    results = r.json['data']
    assert 13 == len(results)

    # Test plural route
    r = client.get('/persons/2')
    assert 200 == r.status_code
    results = r.json
    assert 29 == results['age']

    r = client.get('/persons/28')
    assert 200 == r.status_code
    results = r.json
    assert 0 == len(results)

    # Test route filter
    r = client.get('/persons?age=30')
    assert 200 == r.status_code
    results = r.json['data']
    assert 3 == len(results)

    # Test route filter
    r = client.get('/persons?gender=male')
    assert 200 == r.status_code
    results = r.json['data']
    assert 7 == len(results)

    # Test route two filters
    r = client.get('/persons?gender=female&age=30')
    assert 200 == r.status_code
    results = r.json['data']
    assert 1 == len(results)

    # Test route sort
    r = client.get('/persons?_sort=age')
    assert 200 == r.status_code
    results = r.json['data']
    assert 13 == len(results)
    assert 21 == results[0]['age']

    # Test route sort
    r = client.get('/persons?_sort=name')
    assert 200 == r.status_code
    results = r.json['data']
    assert 13 == len(results)
    assert "Anastasia Coffey" == results[0]['name']

    # Test route sort and order
    r = client.get('/persons?_sort=age&_order=desc')
    assert 200 == r.status_code
    results = r.json['data']
    assert 13 == len(results)
    assert 39 == results[0]['age']

    # Test route paginate
    r = client.get('/persons?_page=1')
    assert 200 == r.status_code
    results = r.json['data']
    assert 10 == len(results)

    r = client.get('/persons?_page=2')
    assert 200 == r.status_code
    results = r.json['data']
    assert 3 == len(results)

    # Test route paginate and limit
    r = client.get('/persons?_page=4&_limit=4')
    assert 200 == r.status_code
    results = r.json['data']
    assert 1 == len(results)
