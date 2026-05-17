import pathlib
import json


ROOM_SIZE = []
NAMES = []
SIZES = []


def _load_room(data):
    global ROOM_SIZE

    ROOM_SIZE = data["room_size"]

def _load_names(data):
    for rectangle_data in data["rectangles"]:
        size = rectangle_data["name"]
        NAMES.append(size)

def _load_sizes(data):
    for rectangle_data in data["rectangles"]:
        size = rectangle_data["size"]
        SIZES.append(size)

def load_problem(path_string):
    path = pathlib.Path(path_string)

    try:
        with open(path) as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        print(f"{path} doesn't exist.")
        return None
    except json.JSONDecodeError as e:
        print(f"{path} is not a valid JSON file: {e}")
        return None

    _load_room(data)
    _load_names(data)
    _load_sizes(data)
