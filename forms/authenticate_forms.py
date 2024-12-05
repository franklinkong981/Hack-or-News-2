"""This is the file where the forms dealing with user authentication are defined, specifically the forms for signing up and logging in."""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Optional, ValidationError
import validators

# Custom validator to make sure profile picture URL corresponds to an actual valid not-malformed image.
def url_corresponding_to_image_check(form, field):
  """First, checks to see if it's a valid URL. Then checks to see if it's a valid image URL. 3 file formats accepted are .jpg,
  .png, and .svg. Thus, either the URL ends with one of these extensions or the extension is right before the query string."""
  
  url = field.data
  if not validators.url(url):
    raise ValidationError("Must be a valid URL!")
  
  url_without_query_string = url if url.find('?') == -1 else url[:url.find('?')]
  if not url_without_query_string.endswith(('.jpg', '.png', '.svg')):
    raise ValidationError("URL must correspond to either a .jpg, .png, or .svg image")


class SignupForm(FlaskForm):
  """User must provide a unique username that's no more than 50 characters, unique email,
  optional profile picture URL, and a password that's at least 8 characters long."""

  username = StringField('Username (at most 50 characters) *', validators=[DataRequired(message="You must provide a username!"), Length(max=50, message="Your username can't be more than 50 characters long!")])
  email = StringField('Email *', validators=[DataRequired(message="You must provide an email!"), Email("You must provide a valid email address! Make sure the email is in the proper format.")])
  profile_picture_url = StringField('Profile Picture URL', validators=[Optional(), url_corresponding_to_image_check])
  password = PasswordField('Password (at least 8 characters) *', validators=[DataRequired(message="You must provide a password!"), Length(min=8, message="Your password must be at least 8 characters long!")])

class LoginForm(FlaskForm):
  """Don't want validators in login form to prevent giving hackers hints."""
  username = StringField('Username *', validators=[DataRequired(message="Please enter your username!")])
  password = PasswordField('Password *', validators=[DataRequired(message="Please enter your password!")])
  