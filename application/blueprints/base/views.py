import json

from flask import (
  render_template,
  Blueprint,
  current_app)


base = Blueprint('base', __name__)

def read_json_file(data_file_path):
  f = open(data_file_path,)
  data = json.load(f)
  f.close()
  return data


@base.route('/')
@base.route('/index')
def index():
  return render_template('index.html')

@base.route('/about/<name>')
def about(name):
  return render_template('index.html', name=name)

@base.route('/resource')
@base.route('/resource/')
@base.route('/resource/<id>')
def resource(id):
  # proposed interface
  data = read_json_file("application/data/resource.json")
  return render_template('resource.html', id=id, resource=data)