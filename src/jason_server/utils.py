
from itertools import islice
import json


def open_database(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("< {0} > does not exists.".format(path))
        exit(1)
    except json.JSONDecodeError:
        print("< {0} > is not well formated.".format(path))
        exit(2)


def chunk_list(data, chunk_size=1):
    it = iter(data)
    return iter(lambda: tuple(islice(it, chunk_size)), ())
