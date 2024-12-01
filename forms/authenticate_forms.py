"""This is the file where the forms dealing with user authentication are defined, specifically the forms for signing up and logging in."""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Optional

class SignupForm(FlaskForm):
  """User must provide a unique username that's no more than 50 characters, unique email,
  optional profile picture URL, and a password that's at least 8 characters long."""

  username = StringField('Username:', validators=[DataRequired(message="You must provide a username!"), Length(max=50, message="Your username can't be more than 50 characters long!")])
  email = StringField('Email: ', validators=[DataRequired(message="You must provide an email!"), Email("You must provide a valid email address!")])
  profile_picture_url = StringField('Profile Image URL (optional):', validators=[Optional()])
  password = PasswordField('Password:', validators=[DataRequired(message="You must provide a password!"), Length(min=8, message="Your password must be at least 8 characters long!")])

class LoginForm(FlaskForm):
  """Don't want validators in login form to prevent giving hackers hints."""
  username = StringField('Username:', validators=[DataRequired(message="Please enter your username!")])
  password = PasswordField('Password:', validators=[DataRequired(message="Please enter your password!")])
  