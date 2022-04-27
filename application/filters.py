import json

def hex_to_rgb_string(hex):
    h = hex.lstrip("#")
    rgb = tuple(int(h[i: i + 2], 16) for i in (0, 2, 4))
    return f"{rgb[0]},{rgb[1]},{rgb[2]}"

def debug(thing):
  return f"<script>console.log({json.dumps(thing)});</script>"
