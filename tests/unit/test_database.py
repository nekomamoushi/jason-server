
from jason_server.database import Database

NON_EXISTING_FILE = "tests/data/non_existing_file"
BAD_FORMATTED_FILE = "tests/data/bad_formatted_database.json"
JSON_DATABASE = "tests/data/sample_database.json"


def describe_database():

    def with_existing_database():
        db = Database(path=JSON_DATABASE)
        assert 2 == len(db.endpoints)
        assert 'articles' in db.endpoints
        assert 'authors' in db.endpoints
        assert 2 == len(db.resources())
        assert 2 == len(db.resource('articles'))
        assert 3 == len(db.resource('authors'))
