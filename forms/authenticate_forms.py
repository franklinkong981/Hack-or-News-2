"""This is the file where the forms dealing with user authentication are defined, specifically the forms for signing up and logging in."""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Optional, ValidationError
import validators

# Custom validator to make sure profile picture URL corresponds to an actual valid not-malformed URL. Uses Python validators package.
def url_check(form, field):
  if not validators.url(field.data):
    raise ValidationError("Must be a valid URL!")

class SignupForm(FlaskForm):
  """User must provide a unique username that's no more than 50 characters, unique email,
  optional profile picture URL, and a password that's at least 8 characters long."""

  username = StringField('Username (at most 50 characters):', validators=[DataRequired(message="You must provide a username!"), Length(max=50, message="Your username can't be more than 50 characters long!")])
  email = StringField('Email: ', validators=[DataRequired(message="You must provide an email!"), Email("You must provide a valid email address! Make sure the email is in the proper format.")])
  profile_picture_url = StringField('Profile Image URL (optional):', validators=[Optional(), url_check])
  password = PasswordField('Password (at least 8 characters):', validators=[DataRequired(message="You must provide a password!"), Length(min=8, message="Your password must be at least 8 characters long!")])

class LoginForm(FlaskForm):
  """Don't want validators in login form to prevent giving hackers hints."""
  username = StringField('Username:', validators=[DataRequired(message="Please enter your username!")])
  password = PasswordField('Password:', validators=[DataRequired(message="Please enter your password!")])
  