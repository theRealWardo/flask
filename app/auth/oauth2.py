from app import oauth
from app import db
from app.auth.models import User
from app.auth.models import Client
from app.auth.models import Grant
from app.auth.models import Token
from datetime import datetime, timedelta
from flask import session
from flask import request
from flask import render_template, redirect, jsonify
from flask import Blueprint
from werkzeug import check_password_hash
from werkzeug.security import gen_salt


mod_oauth = Blueprint('oauth', __name__, url_prefix='/oauth')

REDIRECT_URI = 'http://172.28.128.3:8880/webauth/complete'


def try_login(form):
  if form and form.get('password') and form.get('email'):
    user = User.query.filter_by(email=form.get('email')).first()
    if user and check_password_hash(user.password, form.get('password')):
      return user
  return None


@oauth.usergetter
def get_user(username, password, client, request,
    *args, **kwargs):
  user = User.query.filter_by(email=username).first()
  if user and check_password_hash(user.password, password):
    return user
  return None


def current_user():
  if 'user_id' in session:
    uid = session['user_id']
    return User.query.get(uid)
  return None


@oauth.clientgetter
def load_client(client_id):
  return Client.query.filter_by(client_id=client_id).first()


@oauth.grantgetter
def load_grant(client_id, code):
  return Grant.query.filter_by(client_id=client_id, code=code).first()


@oauth.grantsetter
def save_grant(client_id, code, oauth_request, *args, **kwargs):
  if 'password' in dict(oauth_request.uri_query_params):
    # GET
    user = try_login(dict(oauth_request.uri_query_params))
  elif 'password' in dict(oauth_request.decoded_body):
    # POST
    user = try_login(dict(oauth_request.decoded_body))
  else:
    # 3rd party web
    user = current_user()
  # decide the expires time yourself
  expires = datetime.utcnow() + timedelta(seconds=100)
  grant = Grant(
      client_id=client_id,
      code=code['code'],
      redirect_uri=oauth_request.redirect_uri,
      _scopes=' '.join(oauth_request.scopes),
      user=user,
      expires=expires,
  )
  db.session.add(grant)
  db.session.commit()
  return grant


@oauth.tokengetter
def load_token(access_token=None, refresh_token=None):
  if access_token:
    return Token.query.filter_by(access_token=access_token).first()
  elif refresh_token:
    return Token.query.filter_by(refresh_token=refresh_token).first()


@oauth.tokensetter
def save_token(token, oauth_request, *args, **kwargs):
  toks = Token.query.filter_by(
      client_id=oauth_request.client.client_id,
      user_id=oauth_request.user.id
  )
  # make sure that every client has only one token connected to a user
  for t in toks:
    db.session.delete(t)

  expires_in = token.pop('expires_in')
  expires = datetime.utcnow() + timedelta(seconds=expires_in)

  tok = Token(
      access_token=token['access_token'],
      refresh_token=token['refresh_token'],
      token_type=token['token_type'],
      _scopes=token['scope'],
      expires=expires,
      client_id=oauth_request.client.client_id,
      user_id=oauth_request.user.id,
  )
  db.session.add(tok)
  db.session.commit()
  return tok


@mod_oauth.route('/token')
@oauth.token_handler
def access_token():
  return None


@mod_oauth.route('/authorize', methods=['GET', 'POST'])
@oauth.authorize_handler
def authorize(*args, **kwargs):
  user = try_login(request.values) or current_user()
  if request.values.get('firstparty') == 'yes':
    if user:
      return True
    else:
      return False
  if not user:
    return redirect('/')
  if request.method == 'GET':
    client_id = kwargs.get('client_id')
    client = Client.query.filter_by(client_id=client_id).first()
    kwargs['client'] = client
    kwargs['user'] = user
    return render_template('authorize.html', **kwargs)
  confirm = request.form.get('confirm', 'no')
  return confirm == 'yes'


@mod_oauth.route('/api/me')
@oauth.require_oauth()
def me():
  user = request.oauth.user
  return jsonify(username=user.name)


@mod_oauth.route('/client')
def client():
  user = current_user()
  if not user:
    return redirect('/')
  item = Client(
      client_id=gen_salt(40),
      client_secret=gen_salt(50),
      _redirect_uris=' '.join([REDIRECT_URI]),
      _default_scopes='email',
      user_id=user.id,
  )
  db.session.add(item)
  db.session.commit()
  return jsonify(
    client_id=item.client_id,
    client_secret=item.client_secret,
  )
