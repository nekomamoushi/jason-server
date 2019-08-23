import os
from functools import reduce

import bottle
from bottle import Bottle, template, request, response
from tinydb import where

from jason_server.database import Database
from jason_server.utils import chunk_list, str_to_int

# --------------------------------------------------------------------------- #

# Define base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# App Config
bottle.TEMPLATE_PATH.insert(0, os.path.join(BASE_DIR, 'views'))

app = Bottle()
db = None

# --------------------------------------------------------------------------- #


def build_link_header(request, page, total):

    REL_FIRST = '<{url}?_page={first}>; rel="first"'
    REL_PREV = '<{url}?_page={prev}>; rel="prev"'
    REL_NEXT = '<{url}?_page={next}>; rel="next"'
    REL_LAST = '<{url}?_page={last}>; rel="last"'

    scheme, netloc, path = request.urlparts[0:3]
    url = "{scheme}://{netloc}{path}".format(
        scheme=scheme,
        netloc=netloc,
        path=path
    )
    links = None

    if total == 1:
        return ""

    if page == 1:
        links = [
            REL_FIRST.format(url=url, first=1),
            REL_NEXT.format(url=url, next=2),
            REL_LAST.format(url=url, last=total)
        ]
    elif page == total:
        links = [
            REL_FIRST.format(url=url, first=1),
            REL_PREV.format(url=url, prev=total-1),
            REL_LAST.format(url=url, last=total)
        ]
        return ",".join(links)
    else:
        links = [
            REL_FIRST.format(url=url, first=1),
            REL_PREV.format(url=url, prev=page-1),
            REL_NEXT.format(url=url, next=page+1),
            REL_LAST.format(url=url, last=total)
        ]

    return ",".join(links)


def query_filter(table, arguments):
    user_arguments = [
        (k, v)
        for k, v in arguments.items()
        if not k.startswith('_')
    ]
    if not user_arguments:
        return table.all()

    query = [where(k) == str_to_int(v) for k, v in user_arguments]

    resources = table.search(reduce(lambda a, b: a & b, query))

    return resources


def query_sort(resources, arguments):
    if '_sort' not in arguments:
        return resources

    sort = arguments['_sort']
    order = 'asc' if '_order' not in arguments else arguments['_order']
    if order == 'asc':
        return sorted(resources, key=lambda i: i[sort])

    return sorted(resources, key=lambda i: i[sort], reverse=True)


def query_paginate(resources, arguments):
    if '_page' not in arguments:
        return resources

    page = int(arguments['_page'])
    limit = 10 if '_limit' not in arguments else int(arguments['_limit'])
    chunk_data = list(chunk_list(resources, limit))
    results = chunk_data[page-1]
    link_header = build_link_header(request, page, len(chunk_data))
    response.set_header("Link", link_header)
    return results


def retrieve_resources(endpoint, arguments=None):

    table = db.resource(endpoint)

    if not arguments:
        return dict(data=table.all())

    results = query_filter(table, request.query)
    results = query_sort(results, request.query)
    results = query_paginate(results, request.query)

    return dict(data=results)


def retrieve_resource(endpoint, index):
    table = db.resource(endpoint)
    elements = table.all()
    index = int(index) - 1

    if index >= len(elements):
        return {}

    return elements[index]


# --------------------------------------------------------------------------- #

@app.hook('after_request')
def set_default_headers():
    response.set_header("X-Powerded-By", "Bottle")


@app.route('/')
def bottle_world():

    def build_url(host, port):
        return "http://{}:{}".format(host, port)

    host = app.config.get('host')
    port = app.config.get('port')
    resources = {
        "base_url": build_url(host, port),
        "tables": db.endpoints
    }
    return template('index.html', resources)


@app.route('/db')
def db():
    return db.json


@app.route('/<endpoint>', method='GET')
def get_resources(endpoint):
    results = retrieve_resources(endpoint, request.query)
    return results


@app.route('/<endpoint>/<index>', method='GET')
def get_resource(endpoint, index):
    resource = retrieve_resource(endpoint, index)
    return resource

# --------------------------------------------------------------------------- #


def print_message(database, tables, host, port):
    BOLD_BLUE = '\033[1;34m'
    RESET = '\033[0m'

    print("\n    {}Database{}".format(BOLD_BLUE, RESET))
    print("    {}".format(database))

    print("\n    {}Resources{}".format(BOLD_BLUE, RESET))
    base_url = "http://{}:{}".format(host, port)
    for table in tables:
        print("    {}/{}".format(base_url, table))

    print("\n    {}Home{}".format(BOLD_BLUE, RESET))
    print("    {}/".format(base_url))


def create_database(path, host='localhost', port=8080):
    app.config.setdefault('host', host)
    app.config.setdefault('port', port)
    global db
    db = Database(path)


def run(options, database):
    host = options['host']
    port = options['port']
    quiet = options['quiet']

    app.config.setdefault('host', host)
    app.config.setdefault('port', port)
    global db
    db = Database(database)
    if not quiet:
        print_message(database, db.endpoints, host, port)
    app.run(host=host, port=port, quiet=True)
