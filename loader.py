import pathlib
import json


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

    return data
