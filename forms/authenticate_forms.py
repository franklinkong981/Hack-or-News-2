"""This is the file where the forms dealing with user authentication are defined, specifically the forms for signing up and logging in."""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Optional

class SignupForm(FlaskForm):
  """Defines form for user signing up. User must provide a username that's no more than 50 characters, email that's a valid email,
  optional profile picture URL, and a password that's at least 8 characters long."""

  username = StringField('Username:', validators=[DataRequired(message="You must provide a username!"), Length(max=50, message="Your username can't be more than 50 characters long!")])
  email = StringField('Email: ', validators=[DataRequired(message="You must provide an email!"), Email("You must provide a valid email address!")])
  profile_picture_url = StringField('Profile Image URL (optional):', validators=[Optional()])
  password = PasswordField('Password:', validators=[DataRequired(message="You must provide a password!"), Length(min=8, message="Your password must be at least 8 characters long!")])

  