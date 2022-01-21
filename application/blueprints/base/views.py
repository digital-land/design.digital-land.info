import json
import os

from flask import render_template, Blueprint, current_app, redirect, url_for

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
@base.route('/', defaults={'path': 'index'})
@base.route("/<path:path>")
def match_template(path):

    # if URL ends in a slash append index.html
    if path[-1] == '/':
        path += 'index.html'
    # otherwise just append.html
    else:
        path += '.html'

    file = 'application/templates/' + path

    print('look for: ', path, file)
    if os.path.exists(file):
        return render_template(path)
    
    # else go to homepage
    return redirect(url_for('base.notemplate')) 

@base.route("/template-note-found")
def notemplate():
    return render_template("pages/no-template.html")

@base.route("/index")
def index():
    return render_template("index.html")

@base.route("/homepage")
def homepage():
    return render_template("pages/homepage.html")

@base.route("/about/<name>")
def about(name):
    return render_template("index.html", name=name)

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
