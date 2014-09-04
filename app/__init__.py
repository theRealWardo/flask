from flask import Flask, render_template

from flask.ext.admin import Admin
from flask.ext.sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from app.auth.controllers import mod_auth as auth_module

# Register blueprint(s)
app.register_blueprint(auth_module)
# app.register_blueprint(xyz_module)
# ..


# Admin
from app.admin import controllers as admin_controllers
admin_module = Admin(app, 'GoGo Cal Admin')
admin_controllers.register(admin_module)


# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()
