from bottle import Bottle, run
from bottle import template
from jason_server.database import get_table, generate_endpoints, get_tiny_table_names

# ---------------------------------------------------------------------------- #

INDEX_TEMPLATE="""
<html>
    <head><title>Jason Server</title></head>
    <body>
        <h1>Resources</h1>
        <ul>
        % for table in tables:
            <li>
                <a href="{{base_url}}/{{table}}">{{table}}</a>
            </li>
        % end
        </ul>
        <h1>HTTP Method:</h1>
        <ul>
            <li>GET</li>
        </ul>
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

def run(options, database):
    host = options['host']
    port = options['port']
    app.config.setdefault('host', host)
    app.config.setdefault('port', port)
    generate_endpoints(database)
    app.run(host=host, port=port)
