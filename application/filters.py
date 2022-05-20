import json
import jsonpickle

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
