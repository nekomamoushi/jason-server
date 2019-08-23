
from itertools import islice
import json

try:
    FileNotFoundError
except:
    FileNotFoundError = IOError

try:
    from json.decoder import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError


def open_database(path):
    """Return JSON database as Python Dict

    Args:
        path(str): path to database

    Returns:
        dict: Objectrepresentation of the database

    """
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("< {0} > does not exists.".format(path))
        exit(1)
    except JSONDecodeError:
        print("< {0} > is not well formated.".format(path))
        exit(2)


def chunk_list(data, chunk_size=1):
    """Chunk list into smaller lists

    Args:
        data(list): list to chunk
    Returns:
        list: smaller lists

    """
    it = iter(data)
    return iter(lambda: tuple(islice(it, chunk_size)), ())


def str_to_int(value):
    """Convert str to int if possible

    Args:
        value(str): string to convert
    Returns:
        int: converted value. str otherwise

    """
    try:
        return int(value)
    except ValueError:
        return value
