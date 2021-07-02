#!/usr/bin/env python

from flask import Flask
from flask_script import Manager

from app.factory import create_app

app = Flask(__name__)

manager = Manager(create_app)

if __name__ == "__main__":
    manager.run()

