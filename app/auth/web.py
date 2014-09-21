"""The /webauth/* endpoints responsible for web authentication.

This code handles redirecting the web client appropriately through
the login flow. A successful login looks like:
  POST /webauth/signin
  GET /oauth/authorize?response_type=code&client_id=...
  GET /webauth/complete?code=...
  GET /oauth/token?grant_type=authorization_code&code=...
After 3 nice 302s you end up with a OAuth token that the client
then uses to talk to all the APIs.

Ideally, the final token part of this needs to be done on the server
to ensure protection of our web client secret (and thus prevent spoofing).
"""
from flask import Blueprint
from flask import jsonify
from flask import redirect
from flask import request
from flask import session
from flask import url_for
from flask_oauthlib.client import OAuth
from flask_oauthlib.utils import extract_params

from app import app
from app import oauth

mod_auth_web = Blueprint('webauth', __name__, url_prefix='/webauth')

oauth_client = OAuth(app)

CLIENT_ID = 'bmK1FMxiesLmKDh9qTjocdZFV0bijdDu65OOp5ZB'
CLIENT_SECRET = 'FnoXppxBFq5oo4uqXTPf61Br8FSmmdiMlfXlRoYoDCcmJgzVdn'
APP_NAME = 'remote'

remote = oauth_client.remote_app(
    APP_NAME,
    consumer_key=CLIENT_ID,
    consumer_secret=CLIENT_SECRET,
    request_token_params={'scope': 'email'},
    base_url='http://172.28.128.3:8880/oauth/api/',
    request_token_url=None,
    access_token_url='http://172.28.128.3:8880/oauth/token',
    authorize_url='http://172.28.128.3:8880/oauth/authorize'
)


@mod_auth_web.route('/signin', methods=['POST'])
def signin():
  form = request.get_json()
  # Rather than returning this 302, we could just handle via placing the request
  # on the server side. That would probably be a bit cleaner.
  return remote.authorize(
      callback=url_for('webauth.complete', _external=True),
      email=form.get('email'),
      password=form.get('password'),
      firstparty='yes')


@mod_auth_web.route('/complete', methods=['GET'])
def complete():
  if request.values.get('code'):
    # When the client completes the request for a token, 302 through to
    # get the actual access token.
    remote_args = {
        'code': request.args.get('code'),
        'client_secret': CLIENT_SECRET,
        'redirect_uri': session.get('%s_oauthredir' % APP_NAME)
    }
    remote_args.update(remote.access_token_params)
    client = remote.make_client()
    qs = client.prepare_request_body(**remote_args)
    url = remote.expand_url(remote.access_token_url)
    url += ('?' in url and '&' or '?') + qs
    return redirect(url)
  else:
    return jsonify({
      'status': 'error',
      'error': _get_error_message(request.values.get('error')),
    })


def _get_error_message(error):
  if error == 'access_denied':
    return 'Invalid email or password.'
  else:
    return 'An unknown erorr occurred. Please try again later.'
