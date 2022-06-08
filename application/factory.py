# -*- coding: utf-8 -*-
"""
Flask app factory class
"""
from application.filters import unhyphenate
from flask import Flask
from flask.cli import load_dotenv

load_dotenv()


def create_app(config_filename):
    """
    App factory function
    """
    app = Flask(__name__)
    app.config.from_object(config_filename)
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 10

    register_blueprints(app)
    register_context_processors(app)
    register_templates(app)
    register_filters(app)
    register_extensions(app)

    return app


def register_blueprints(app):
    """
    Import and register blueprints
    """

    from application.blueprints.base.views import base

    app.register_blueprint(base)


def register_context_processors(app):
    """
    Add template context variables and functions
    """

    def base_context_processor():
        return {"assetPath": "/static"}

    app.context_processor(base_context_processor)


def register_filters(app):
    from application.filters import hex_to_rgb_string, debug, get_items_beginning_with, from_json, import_csv

    app.add_template_filter(hex_to_rgb_string, name="hex_to_rgb")
    app.add_template_filter(debug, name="debug")
    app.add_template_filter(get_items_beginning_with, name="get_items_beginning_with")
    app.add_template_filter(unhyphenate, name="unhyphenate")
    app.add_template_filter(from_json, name="from_json")
    app.add_template_filter(import_csv, name="import_csv")


def register_extensions(app):
    """
    Import and register flask extensions and initialize with app object
    """
    pass


def register_templates(app):
    """
    Register templates from packages
    """
    from jinja2 import PackageLoader, PrefixLoader, ChoiceLoader, FileSystemLoader

    multi_loader = ChoiceLoader(
        [
            app.jinja_loader,
            PrefixLoader(
                {
                    "relative_path": FileSystemLoader(searchpath="/"),
                    "govuk_frontend_jinja": PackageLoader("govuk_frontend_jinja"),
                    "digital-land-frontend": PackageLoader("digital_land_frontend"),
                }
            ),
        ]
    )
    app.jinja_loader = multi_loader
