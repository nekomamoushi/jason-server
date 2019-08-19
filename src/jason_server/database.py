
import json

from tinydb import TinyDB
from tinydb.storages import MemoryStorage

from jason_server.utils import open_database

db = TinyDB(storage=MemoryStorage)

def create_table(name):
    return db.table(name)

def populate_table(table, data):
    table_name = table.name
    for elt in data:
        table.insert(elt)

def get_tables(database):
    return [ name for name in database]

def get_table(name):
    return db.table(name)

def generate_endpoints(database_path):
    database = open_database(database_path)
    tables_names = get_tables(database)
    for name in tables_names:
        table = create_table(name)
        populate_table(table, database[name])

