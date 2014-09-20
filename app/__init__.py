import os

from flask import Flask
from flask.ext.admin import Admin
from flask.ext.sqlalchemy import SQLAlchemy

from flask_oauthlib.provider import OAuth2Provider


# App setup.
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
oauth = OAuth2Provider(app)


# 404 and static routing.
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


# Blueprint based modules.
from app.auth.controllers import mod_auth as auth_module
app.register_blueprint(auth_module)

from app.auth.oauth2 import mod_oauth as oauth_module
app.register_blueprint(oauth_module)

from app.auth.web import mod_auth_web as web_module
app.register_blueprint(web_module)


# Flask-Admin module.
from app.admin import controllers as admin_controllers
admin_module = Admin(app, 'Super Awesome Admin')
admin_controllers.register(admin_module)


db.create_all()
