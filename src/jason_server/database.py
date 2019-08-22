
from tinydb import TinyDB
from tinydb.storages import MemoryStorage

from jason_server.utils import open_database

# --------------------------------------------------------------------------- #


def tinydb_make_table(db, name):
    return db.table(name)


def tinydb_populate_table(table, data):
    for elt in data:
        table.insert(elt)

# --------------------------------------------------------------------------- #


class Database(object):

    def __init__(self, path):
        self._path = path
        self._db = TinyDB(storage=MemoryStorage)
        self._json = open_database(path)
        self._endpoints = self._generate_tables()

    def _generate_tables(self):
        resources = [name for name in self._json]
        for name in resources:
            table = tinydb_make_table(self._db, name)
            tinydb_populate_table(table, self._json[name])
        return resources

    @property
    def json(self):
        return self._json

    @property
    def endpoints(self):
        return self._endpoints

    def resources(self):
        return [table for table in self._db.tables() if table != "_default"]

    def resource(self, name):
        return self._db.table(name)
