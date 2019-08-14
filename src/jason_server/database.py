
import json

from tinydb import TinyDB
from tinydb.storages import MemoryStorage

db = TinyDB(storage=MemoryStorage)

def load_database(path):
    with open(path, "r") as f:
        return json.load(f)

def create_table(name):
    return db.table(name)

def populate_table(table, data):
    table_name = table.name
    for elt in data:
        table.insert(elt)

def get_tables(database):
    return [ name for name in database]

def generate_endpoints(database_path):
    database = load_database(database_path)
    tables_names = get_tables(database)
    for name in tables_names:
        table = create_table(name)
        populate_table(table, database[name])

