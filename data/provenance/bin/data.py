#!/usr/bin/env python3

import requests
import json
import hashlib

entities = ["3030363", "192", "16", "329", "144"]

# until we resolve primary/secondary source ..
patches = (
    ("3030363", "reference", "CA01"),
    ("3030363", "organisation-entity", "192"),
    ("3030363", "organisation", "local-authority-eng:LBH"),
)

# pipeline should provide these ..
references = {
    "5336": "3030363",
    "COA00000265": "3030363",
    "CA01": "3030363",
    "53": "3030363",
}

data = {
    "dataset": {},
    "entity": {},
    "fact": {},
    "resource": {},
    "source": {},
    "endpoint": {},
    "curie": {},
}


def fact_hash(entity, field, value):
    data = f"{entity}:{field}:{value}"
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def get(url):
    print(url)
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def entity_curie(entity):
    e = data["entity"][entity]
    return f'{e["prefix"]}:{e["reference"]}'


# load entities
for entity in entities:
    # API currently doesn't return the geometry and point
    o = get(f"https://www.digital-land.info/entity/{entity}.json")
    o["entity"] = str(o["entity"])
    data["entity"][entity] = o
    data["dataset"].setdefault(o["dataset"], {})


for entity in entities:
    # hoist any json elements ..
    e = data["entity"][entity]
    if "json" in e:
        for field, value in e["json"].items():
            e[field] = value
        del e["json"]

    if "geojson" in e and "properties" in e["geojson"]:
        del e["geojson"]["properties"]

    # default the organisation
    if e["organisation-entity"] and not e.get("organisation", ""):
        e["organisation"] = entity_curie(e["organisation-entity"])


# load entity properties missing from the current JSON
for entity in entities:
    dataset = data["entity"][entity]["dataset"]
    e = get(
        f"https://datasette.digital-land.info/{dataset}/entity.json?entity__exact={entity}&_shape=object"
    )
    if e:
        data["entity"][entity]["geometry"] = e[entity]["geometry"]
        data["entity"][entity]["point"] = e[entity]["point"]


# load entity facts
for entity in entities:
    dataset = data["entity"][entity]["dataset"]
    r = get(
        f"https://datasette.digital-land.info/{dataset}/fact.json?entity__exact={entity}&_shape=object"
    )
    if r:
        for fact, s in r.items():
            o = {}
            for field, value in s.items():
                o[field.replace("_", "-")] = str(value)
            data["fact"][fact] = o

            # add fact to entity
            p = data["entity"][o["entity"]].setdefault("provenance", {
                "resource" : set(),
                "organisation": set(),
                "field-fact": {},
                "fact-field": {}})
            p["fact-field"][o["fact"]] = o["field"]
            if data["entity"][o["entity"]][o["field"]] == o["value"]:
                p["field-fact"][o["field"]] = o["fact"]


    # load fact resources
    r = get(
        f"https://datasette.digital-land.info/{dataset}.json?sql=select+fact.fact%2C+resource+from+fact%2C+fact_resource+where+fact.entity+%3D+%3Ap0+and+fact_resource.fact+%3D+fact.fact&p0={entity}"
    )
    if r:
        for fact, resource in r["rows"]:
            data["fact"][fact].setdefault("resource", [])
            data["fact"][fact]["resource"].append(resource)
            data["resource"].setdefault(resource, {})

# list of resources
resources = ""
sep = ""
for resource in data["resource"]:
    resources += f"{sep}%22{resource}%22"
    sep = "%2C"

# get logs
fields = [
    "resource",
    "status",
    "bytes",
    "content-type",
    "elapsed",
    "endpoint",
    "entry-date",
    "resource",
    "status",
]
field_list = "%2C".join(fields).replace("-", "_")
r = get(
    f"https://datasette.digital-land.info/digital-land.json?sql=select+{field_list}+from+log+where+%22resource%22+in+%28{resources}%29"
)
for row in r["rows"]:
    o = dict(zip(fields, row))
    date = o["entry-date"][:10]
    resource = o["resource"]
    data["resource"][resource].setdefault("log", {})
    data["resource"][resource]["log"][date] = o


# add resource-organisation
fields = [
    "resource",
    "organisation",
]
field_list = "%2C".join(fields).replace("-", "_")
r = get(
    f"https://datasette.digital-land.info/digital-land.json?sql=select+{field_list}+from+resource_organisation+where+resource+in+%28{resources}%29"
)
for row in r["rows"]:
    o = dict(zip(fields, row))
    resource = o["resource"]
    data["resource"][resource].setdefault("organisation", set())
    data["resource"][resource]["organisation"].add(o["organisation"])


# add dataset-resource
fields = [
    "resource",
    "entry-date",
    "entity-count",
    "entry-count",
    "line-count",
    "mime-type",
    "internal-path",
    "internal-mime-type",
]
field_list = "%2C".join(fields).replace("-", "_")
for dataset in data["dataset"]:
    r = get(f"https://datasette.digital-land.info/{dataset}.json?sql=select+{field_list}+from+dataset_resource+where+%22resource%22+in+%28{resources}%29")
    if r:
        for row in r["rows"]:
            o = dict(zip(fields, row))
            resource = o["resource"]
            data["resource"][resource].setdefault("dataset", {})
            data["resource"][resource]["dataset"][dataset] = o

# add resources and organisations to each entity
for fact, f in data["fact"].items():
    for resource in f["resource"]:
        data["entity"][f["entity"]]["provenance"]["resource"].add(resource)
        for organisation in data["resource"][resource]["organisation"]:
            data["entity"][f["entity"]]["provenance"]["organisation"].add(organisation)

# patch the data ..
for entity, field, value in patches:
    data["entity"][entity][field] = value

# curie index
for entity in data["entity"]:
    data["curie"][entity_curie(entity)] = entity

# patch fact reference-entity values
references = references | data["curie"]
for fact, f in data["fact"].items():
    if f["value"] in references:
        f["reference-entity"] = references[f["value"]]

# dataset info
for dataset in data["dataset"]:
    o = get(
        f"https://datasette.digital-land.info/digital-land/dataset.json?dataset__exact={dataset}&_shape=object"
    )
    if o:
        data["dataset"][dataset] = o


with open("data.json", "w") as f:
    json.dump(data, f, sort_keys=True, indent=4, default=tuple)
