
import json

def open_database(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError as e:
        print("< {0} > does not exists.".format(path))
        exit(1)
    except json.JSONDecodeError as e:
        print("< {0} > is not well formated.".format(path))
        exit(2)
