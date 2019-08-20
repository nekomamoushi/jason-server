from bottle import Bottle, template
from jason_server.database import get_table, generate_endpoints, get_tiny_table_names

# ---------------------------------------------------------------------------- #

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

# ---------------------------------------------------------------------------- #

app = Bottle()

# ---------------------------------------------------------------------------- #


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
    data = table.all()
    return dict(data=data)

# ---------------------------------------------------------------------------- #


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
    app.config.setdefault('host', host)
    app.config.setdefault('port', port)
    table_names = generate_endpoints(database)
    print_message(database, table_names, host, port)
    app.run(host=host, port=port, quiet=True)
