from bottle import Bottle, run

app = Bottle()

@app.route('/')
def bottle_world():
    return "Bottle World!"

def run(options):
    host = options['host']
    port = options['port']
    app.run(host=host, port=port)
