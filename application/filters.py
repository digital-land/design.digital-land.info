import json
import jsonpickle
import csv
import os
from markdown import markdown
from bs4 import BeautifulSoup

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

def to_markdown(content):
    soup = BeautifulSoup(markdown(content))
    _add_attrs(soup)
    return soup.prettify()

def _add_attrs(soup):
    for tag in soup.select("p"):
        tag['class'] = "govuk-body"
    for tag in soup.select("h1"):
        tag['class'] = "govuk-heading-xl"
    for tag in soup.select("h2"):
        tag['class'] = "govuk-heading-l"
    for tag in soup.select("h3"):
        tag['class'] = "govuk-heading-m"
    for tag in soup.select("h4"):
        tag['class'] = "govuk-heading-s"
    for tag in soup.select("ul"):
        tag['class'] = "govuk-list govuk-list--bullet"
    for tag in soup.select("a"):
        tag['class'] = "govuk-link"
