import os

from flask import Flask, render_template

from flask.ext.admin import Admin
from flask.ext.sqlalchemy import SQLAlchemy

# Build the app. 
app = Flask(__name__)
app.config.from_object('config')
if 'CONFIG_OVERRIDE' in os.environ:
  app.config.from_envvar('CONFIG_OVERRIDE')
db = SQLAlchemy(app)

# Static handlers.
@app.errorhandler(404)
def not_found(error):
    return app.send_static_file('404.html'), 404


@app.route('/')
def index():
  return app.send_static_file('index.html')


@app.route('/js/<path:path>')
def static_js(path):
  return app.send_static_file(os.path.join('js', path))


@app.route('/css/<path:path>')
def static_css(path):
  return app.send_static_file(os.path.join('css', path))


@app.route('/img/<path:path>')
def static_img(path):
  return app.send_static_file(os.path.join('img', path))


@app.route('/templates/<path:path>')
def static_templates(path):
  return app.send_static_file(os.path.join('templates', path))


@app.route('/lib/<path:path>')
def static_lib(path):
  # Map from /static/bower_components/* to /lib/*
  return app.send_static_file(os.path.join('bower_components', path))


@app.route('/build/<path:path>')
def static_build(path):
  return app.send_static_file(os.path.join('build', path))


# Import a module / component using its blueprint handler variable (mod_auth)
from app.auth.controllers import mod_auth as auth_module

# Register blueprint(s)
app.register_blueprint(auth_module)
# app.register_blueprint(xyz_module)
# ..


# Admin
from app.admin import controllers as admin_controllers
admin_module = Admin(app, 'Super Awesome Admin')
admin_controllers.register(admin_module)


# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()
