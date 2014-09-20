from app import db
from app.auth import models as auth_models

from flask.ext.admin.contrib import sqla


def register(admin_module):
  admin_module.add_view(sqla.ModelView(auth_models.User, db.session))
  admin_module.add_view(sqla.ModelView(auth_models.Client, db.session))
