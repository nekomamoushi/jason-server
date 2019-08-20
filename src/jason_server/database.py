
from tinydb import TinyDB
from tinydb.storages import MemoryStorage

from jason_server.utils import open_database

db = TinyDB(storage=MemoryStorage)


def create_table(name):
    return db.table(name)


def populate_table(table, data):
    for elt in data:
        table.insert(elt)


def get_tables(database):
    return [ name for name in database ]


def get_table(name):
    return db.table(name)


def get_tiny_table_names():
    return [ table for table in db.tables() if table != "_default" ]


def generate_endpoints(database_path):
    database = open_database(database_path)
    tables_names = get_tables(database)
    for name in tables_names:
        table = create_table(name)
        populate_table(table, database[name])
    return tables_names
