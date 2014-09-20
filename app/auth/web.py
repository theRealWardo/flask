from flask import Blueprint, request, url_for, jsonify
from flask_oauthlib.client import OAuth
from app import app

mod_auth_web = Blueprint('webauth', __name__, url_prefix='/webauth')

oauth = OAuth(app)

CLIENT_ID = 'us2JPQnxQGTbA60KzND5cHoQTbcaq3Bjvgq8TOEj'
CLIENT_SECRET = 'sx1UvB2HPZ539uJHS62HwIRlmKjmsJXqAWKuI7cVkrOstjHSBo'

remote = oauth.remote_app(
    'remote',
    consumer_key=CLIENT_ID,
    consumer_secret=CLIENT_SECRET,
    request_token_params={'scope': 'email'},
    base_url='http://172.28.128.3:8880/oauth/api/',
    request_token_url=None,
    access_token_url='http://172.28.128.3:8880/oauth/token',
    authorize_url='http://172.28.128.3:8880/oauth/authorize'
)


@mod_auth_web.route('/signin', methods=['GET'])
def signin():
  next_url = '/'
  return remote.authorize(
      callback=url_for('webauth.authorized', _external=True))


@mod_auth_web.route('/authorized')
def authorized():
    resp = remote.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    print resp
    session['remote_oauth'] = (resp['access_token'], '')
    return jsonify(oauth_token=resp['access_token'])
