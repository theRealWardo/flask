"""The /auth/* endpoints responsible for general authentication tasks.

General authentication tasks include almost everything other than signin.
However, note that the profile is separate from the user and therefore is
not part of the auth module. Enabling login with Facebook or Google is
handled here but importing that profile data is not.
"""
from flask import Blueprint
from flask import jsonify
from flask import request
from werkzeug import generate_password_hash

from app import db
from app.auth.forms import SignupForm
from app.auth.models import User

mod_auth = Blueprint('auth', __name__, url_prefix='/auth')


@mod_auth.route('/signup', methods=['POST'])
def signup():
  # TODO(mattward): Figure out what we should do for CSRF prevention.
  form = SignupForm.from_json(request.get_json(), csrf_enabled=False)
  if form.validate():
    user = User(name=form.name.data,
                email=form.email.data,
                password=generate_password_hash(form.password.data))
    s = db.session()
    s.add(user)
    s.commit()
    return jsonify({
      'status': 'ok',
    })
  else:
    errors = [v[0] for k, v in form.errors.items()]
    return jsonify({
      'status': 'error',
      'error': errors[0] if errors else 'An unknown error occurred.',
    })
