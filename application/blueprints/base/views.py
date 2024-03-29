import json
import os

from flask import Blueprint, redirect, render_template, url_for, request

base = Blueprint("base", __name__)

@base.context_processor
def set_globals():
    return {"staticPath": "https://digital-land.github.io"}


def read_json_file(data_file_path):
    f = open(
        data_file_path,
    )
    data = json.load(f)
    f.close()
    return data


# this attempts to take a URL path and render a matching template
@base.route("/", defaults={"path": "index.html"})
@base.route("/<path:path>")
def match_template(path):

    # if URL ends in a slash append index.html
    if path[-1] == "/":
        path += "index.html"
    if path[-1:] != "/" and path[-5:] != ".html":
        path += '/index.html'

    file = "application/templates/" + path

    # this code is a quick and messy was of giving each template
    # a distinc class to hook off when trying different versions
    # of prototypes
    versionClasses = ""
    versionPath = ""
    # split the path variable on '/' slashes
    splitPath = path.split("/")
    # print(splitPath)
    # get length of split path array/list
    length = len(splitPath)

    # if length is 1 then we know we're not in a subdirectory
    if length == 1:
        versionClasses += "agnostic"
    # else assume in a subdirectory for a specific prototype
    else:
        for i in range(length):
            # if item is after the 1st we know it is not the /pages/ directory
            if i > 0:
                versionClasses += splitPath[i]
                if i < length - 1:
                    versionClasses += "-"

    versionClasses = "app-" + versionClasses.replace(".html", "", 1)
    if "prototypes" in splitPath:
        _versionPath = splitPath[:-1]
        for i in range(len(_versionPath)):
            if i <= 2:
                versionPath += f"{_versionPath[i]}/"
        # print("version path ", versionPath)
    else:
        file = file.replace("templates/", "templates/pages/")
        splitPath.insert(0, "pages")
        path = f"pages/{path}"


    # print("look for: ", path, file)
    provenanceData = read_json_file("data/provenance/data.json")
    performanceThing = {
        "local-authority-eng:LBH":{
            "area-of-outstanding-natural-beauty":None,
            "article-4-direction-area":False,
            "central-activities-zone":True,
            "conservation-area":False,
            "listed-building":None,
            "listed-building-outline":False,
            "national-park":None,
            "scheduled-monuments":None,
            "site-of-special-scientific-interest":None,
            "tree-preservation-order":None
        }
    }

    datasets = [
      "area-of-outstanding-natural-beauty",
      "article-4-direction-area",
      "central-activities-zone",
      "conservation-area",
      "listed-building",
      "listed-building-outline",
      "national-park",
      "scheduled-monuments",
      "site-of-special-scientific-interest",
      "tree-preservation-order"
    ]

    pathDir = ""
    pathParentDir = ""
    for thing in range(len(splitPath) -1):
        pathDir += splitPath[thing] + "/"
    for thing in range(len(splitPath) -2):
        pathParentDir += splitPath[thing] + "/"

    pathInfo = {
        'full': path,
        'split': splitPath,
        'dir':pathDir,
        'dirParent': pathParentDir
    }

    qs = request.args;

    if os.path.exists(file):
        return render_template(path, versionClasses=versionClasses, versionPath=versionPath, provenanceData=provenanceData, performanceThing=performanceThing, datasets=datasets, qs=qs, path=pathInfo)

    # else show no template
    return redirect(url_for("base.notemplate"))


@base.route("/template-note-found")
def notemplate():
    return render_template("pages/no-template.html")


@base.route("/homepage")
def homepage():
    return render_template("pages/homepage.html")


@base.route("/entity")
@base.route("/entity/")
def entity():
    return render_template(
        "pages/entity/version-1.html", versionClasses="app-entity-version-1"
    )


@base.route("/resource")
@base.route("/resource/")
@base.route("/resource/<id>")
def resource(id):
    # proposed interface
    data = read_json_file("application/data/resource.json")
    return render_template("pages/resource.html", id=id, resource=data)


@base.route("/resource/no-table")
@base.route("/resource/no-table/<id>")
def resource_no_table(id):
    # proposed interface
    data = read_json_file("application/data/resource.json")
    return render_template("pages/resource-no-table.html", id=id, resource=data)


@base.route("/map")
def map():
    all_layers = [
        # {
        #     "dataset": "local-authority-district",
        #     "label": "Local authority districts",
        #     "paint_options": {"colour": "#0b0c0c", "opacity": "0.1", "weight": 5},
        # },
        {
            "dataset": "brownfield-land",
            "label": "Brownfield land",
            "paint_options": {
                "colour": "#745729",
            },
            "type": "point",
        },
        {
            "dataset": "conservation-area",
            "label": "Conservation areas",
            "paint_options": {
                "colour": "#78AA00",
            },
        },
        {
            "dataset": "open-space",
            "label": "Open spaces",
            "paint_options": {
                "colour": "#5694ca",
            },
        },
    ]
    return render_template("pages/map.html", layers=all_layers)
