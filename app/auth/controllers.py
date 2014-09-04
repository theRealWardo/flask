# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash
from app import db
# Import module forms
from app.auth.forms import LoginForm
from app.auth.forms import SignupForm
# Import module models (i.e. User)
from app.auth.models import User

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

# Set the route and accepted methods
@mod_auth.route('/signin/', methods=['GET', 'POST'])
def signin():
  # If sign in form is submitted
  form = LoginForm(request.form)
  # Verify the sign in form
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user and check_password_hash(user.password, form.password.data):
      session['user_id'] = user.id
      flash('Welcome %s' % user.name)
      return redirect(url_for('auth.home'))
  flash('Wrong email or password', 'error-message')
  return render_template("auth/signin.html", form=form, user_id=session.get('user_id'))

# Set the route and accepted methods
@mod_auth.route('/signup/', methods=['GET', 'POST'])
def signup():
  # If sign in form is submitted
  form = SignupForm(request.form)
  # Verify the sign in form
  if form.validate_on_submit():
    user = User(name=form.name.data,
                email=form.email.data,
                password=generate_password_hash(form.password.data))
    s = db.session()
    s.add(user)
    s.commit()
    return redirect(url_for('auth.signin'))
  return render_template("auth/signup.html", form=form)

# Set the route and accepted methods
@mod_auth.route('/home/', methods=['GET'])
def home():
  if not session.get('user_id'):
    return redirect(url_for('auth.signin'))
  return render_template("auth/home.html", user_id=session['user_id'])
