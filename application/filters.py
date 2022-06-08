import json
import jsonpickle
import csv
import os

basePath = os.path.abspath(os.path.dirname(__file__))

def hex_to_rgb_string(hex):
    h = hex.lstrip("#")
    rgb = tuple(int(h[i: i + 2], 16) for i in (0, 2, 4))
    return f"{rgb[0]},{rgb[1]},{rgb[2]}"

def debug(thing):
  return f"<script>console.log({json.dumps(json.loads(jsonpickle.encode(thing)), indent=2)});</script>"

def unhyphenate(myString):
    tx = myString.replace('-',' ')
    return tx

def get_items_beginning_with(mylist, letter):
  return [item for item in mylist if item[0][0] == letter]


def from_json(data):
    return json.loads(data)


def import_csv(file):
    # https://stackoverflow.com/questions/29432912/convert-a-csv-dictreader-object-to-a-list-of-dictionaries
    filename = f"{basePath}/data/{file}"
    new_dict = ""
    with open(filename) as data:
        new_dict = list(csv.DictReader(data))
    return new_dict
