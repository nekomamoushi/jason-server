from bottle import Bottle, template, request, response
from jason_server.database import (
    get_table,
    generate_endpoints,
    get_tiny_table_names
)
from jason_server.utils import chunk_list

# --------------------------------------------------------------------------- #

INDEX_TEMPLATE = """
<html>
    <head>
        <title>Jason Server</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    </head>
    <body>
        <div class="jumbotron jumbotron-fluid">
            <div class="container">
            <h1>Jason Server</h1>
            </div>
        </div>
        <div class="container">
            <h2>Resources</h2>
            <ul>
                % for table in tables:
                <li>
                    <a href="{{base_url}}/{{table}}">{{table}}</a>
                </li>
                % end
            </ul>
            <h2>HTTP Method supported:</h2>
            <p><span class="badge badge-secondary">GET</span></p>
        </div>
    </body>
</html>
"""

# --------------------------------------------------------------------------- #

app = Bottle()

# --------------------------------------------------------------------------- #

def verify_query_sort(query):
    sort, order = (None, "asc")
    if query and '_sort' in query:
        sort = query['_sort']
        if '_order' in query:
            order = query['_order']
    return sort, order

def verify_query_paginate(query):
    page, limit = (None, 10)
    if query and '_page' in query:
        page = int(query['_page'])
        if '_limit' in query:
            limit = int(query['_limit'])
            limit = limit if limit < 10 else 10

    return page, limit


def build_link_header(request, page, total):

    REL_FIRST = '<{url}?_page={first}>; rel="first"'
    REL_PREV = '<{url}?_page={prev}>; rel="prev"'
    REL_NEXT = '<{url}?_page={next}>; rel="next"'
    REL_LAST = '<{url}?_page={last}>; rel="last"'

    scheme, netloc, path = request.urlparts[0:3]
    url = "{scheme}://{netloc}{path}".format(scheme=scheme, netloc=netloc, path=path)
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
    tables = get_tiny_table_names()
    resources = {
        "base_url": build_url(host, port),
        "tables": tables
    }
    return template(INDEX_TEMPLATE, resources)


@app.route('/<endpoint>', method='GET')
def get(endpoint):
    table = get_table(endpoint)
    data = dict(data=table.all())
    data = data['data']

    if not request.query:
        return dict(data=data)

    results = data

    sort, order = verify_query_sort(request.query)
    if sort:
        if order == 'asc':
            results = sorted(results, key = lambda i: i[sort])
        else:
            results = sorted(results, key = lambda i: i[sort], reverse=True)

    page, limit = verify_query_paginate(request.query)
    if page:
        chunk_data = list(chunk_list(results, limit))
        results = chunk_data[page-1]
        link_header = build_link_header(request, page, len(chunk_data))
        response.set_header("Link", link_header)

    return dict(data=results)

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


def run(options, database):
    host = options['host']
    port = options['port']
    quiet = options['quiet']

    app.config.setdefault('host', host)
    app.config.setdefault('port', port)
    table_names = generate_endpoints(database)
    if not quiet:
        print_message(database, table_names, host, port)
    app.run(host=host, port=port, quiet=True)
