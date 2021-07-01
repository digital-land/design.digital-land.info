#!/usr/bin/env python

from flask import Flask
from flask_script import Manager

from app.factory import create_app
from lib.govuk_assets import ManageGovUkAssets

app = Flask(__name__)

manager = Manager(create_app)
manager.add_command('install_all_govuk_assets', ManageGovUkAssets())

if __name__ == "__main__":
    manager.run()

