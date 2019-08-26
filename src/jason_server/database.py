
from tinydb import TinyDB
from tinydb.storages import MemoryStorage

from jason_server.utils import open_database

# --------------------------------------------------------------------------- #


def tinydb_make_table(db, name):
    """Create Tinydb Table for db

    Args:
        db(Tinydb): database object
        name(str): table name to create

    Returns:
        Table: Table created
    """
    return db.table(name)


def tinydb_populate_table(table, data):
    """Populate Tinydb Table

    Args:
        table(Table): Table object
        data(dict): Resource to inject

    """
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
        """Generate tables from database

        Returns:
            list: table names
        """
        resources = [name for name in self._json]
        for name in resources:
            table = tinydb_make_table(self._db, name)
            tinydb_populate_table(table, self._json[name])
        return resources

    @property
    def json(self):
        """Return Dict Repr for the database

        Returns:
            dict: database as dict
        """
        return self._json

    @property
    def endpoints(self):
        """Return a list of the table's name

        Returns:
            list: table name
        """
        return self._endpoints

    def resources(self):
        """Return a list of the table's name

        Returns:
            list: table name
        """
        return [table for table in self._db.tables() if table != "_default"]

    def resource(self, name):
        """Return the table resource

        Returns:
            Table: Table resource
        """
        return self._db.table(name)
