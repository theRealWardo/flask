# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db

# Define a base model for other database tables to inherit
class Base(db.Model):
  __abstract__  = True

  id = db.Column(db.Integer,
                 primary_key=True)
  date_created = db.Column(db.DateTime,
                           default=db.func.current_timestamp())
  date_modified = db.Column(db.DateTime,
                            default=db.func.current_timestamp(),
                            onupdate=db.func.current_timestamp())


# Define a User model
class User(Base):
  __tablename__ = 'auth_user'
  # User Name
  name = db.Column(db.String(128), 
                   nullable=False)
  # Identification Data: email & password
  email = db.Column(db.String(128),
                    nullable=False,
                    unique=True)
  password = db.Column(db.String(192),
                       nullable=False)

  # New instance instantiation procedure
  def __init__(self, name, email, password):
    self.name = name
    self.email = email
    self.password = password

  def __repr__(self):
    return '<User %r>' % (self.name)                        


# Define an oauth2 client 
class Client(db.Model):
  __tablename__ = 'auth_oauth_client'
  # human readable name, not required
  name = db.Column(db.String(40))
  # human readable description, not required
  description = db.Column(db.String(400))
  # creator of the client, not required
  user_id = db.Column(db.ForeignKey('auth_user.id'))
  # required if you need to support client credential
  user = db.relationship('User')

  client_id = db.Column(db.String(40), primary_key=True)
  client_secret = db.Column(db.String(55), unique=True, index=True, nullable=False)

  # public or confidential
  is_confidential = db.Column(db.Boolean)

  _redirect_uris = db.Column(db.Text)
  _default_scopes = db.Column(db.Text)

  @property
  def client_type(self):
    if self.is_confidential:
      return 'confidential'
    return 'public'

  @property
  def redirect_uris(self):
    if self._redirect_uris:
      return self._redirect_uris.split()
    return []

  @property
  def default_redirect_uri(self):
    return self.redirect_uris[0]

  @property
  def default_scopes(self):
    if self._default_scopes:
      return self._default_scopes.split()
    return []


class Grant(db.Model):
  __tablename__ = 'auth_oauth_grant'
  id = db.Column(db.Integer, primary_key=True)

  user_id = db.Column(db.Integer, db.ForeignKey('auth_user.id', ondelete='CASCADE'))
  user = db.relationship('User')

  client_id = db.Column(db.String(40), db.ForeignKey('auth_oauth_client.client_id'), nullable=False)
  client = db.relationship('Client')

  code = db.Column(db.String(255), index=True, nullable=False)

  redirect_uri = db.Column(db.String(255))
  expires = db.Column(db.DateTime)

  _scopes = db.Column(db.Text)

  def delete(self):
    db.session.delete(self)
    db.session.commit()
    return self

  @property
  def scopes(self):
    if self._scopes:
      return self._scopes.split()
    return []


class Token(db.Model):
  __tablename__ = 'auth_oauth_token'
  id = db.Column(db.Integer, primary_key=True)

  client_id = db.Column(db.String(40), db.ForeignKey('auth_oauth_client.client_id'), nullable=False)
  client = db.relationship('Client')

  user_id = db.Column(db.Integer, db.ForeignKey('auth_user.id'))
  user = db.relationship('User')

  # currently only bearer is supported
  token_type = db.Column(db.String(40))

  access_token = db.Column(db.String(255), unique=True)
  refresh_token = db.Column(db.String(255), unique=True)
  expires = db.Column(db.DateTime)

  _scopes = db.Column(db.Text)

  @property
  def scopes(self):
    if self._scopes:
      return self._scopes.split()
    return []
