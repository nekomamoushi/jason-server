from bottle import Bottle, run
from jason_server.database import get_table, generate_endpoints

app = Bottle()

@app.route('/')
def bottle_world():
    return "Bottle World!"

@app.route('/<endpoint>', method='GET')
def get(endpoint):
    table = get_table(endpoint)
    data = table.all()
    return dict(data=data)

def run(options, database):
    host = options['host']
    port = options['port']
    generate_endpoints(database)
    app.run(host=host, port=port)
