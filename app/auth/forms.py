from flask.ext.wtf import Form

from wtforms import TextField
from wtforms import PasswordField

from wtforms.validators import Required
from wtforms.validators import Email
from wtforms.validators import EqualTo


class LoginForm(Form):
  email = TextField(
      'Email Address',
      [Email(),
       Required(message='Forgot your email address?')])
  password = PasswordField(
      'Password',
      [Required(message='Must provide a password.')])


class SignupForm(Form):
  name = TextField(
      'Name',
      [Required(message='Forgot your name?')])
  email = TextField(
      'Email Address',
      [Email(),
       Required(message='Forgot your email address?')])
  password = PasswordField(
      'Password',
      [Required(message='Must provide a password.')])
