"""This file contains the User model."""

from flask_bcrypt import Bcrypt # For user signup/login password hashing

from models.init_db import db
from datetime import datetime, timezone

bcrypt = Bcrypt()

class User(db.Model):
  """User in the app. A user can create an account by putting down a username (50 characters max), unique email, optional profile picture
  url, and password (at least 8 characters). Once logged in, a user can upload stories."""

  __tablename__ = "users"

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  username = db.Column(db.String(50), nullable=False, unique=True)
  email = db.Column(db.Text, nullable=False, unique=True)
  profile_picture_url = db.Column(db.Text, default="/static/images/default-profile-picture.jpg")
  password = db.Column(db.Text, nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

  def format_created_at(self):
    """Turn the created_at attribute stored in the class into a readable string format."""
    return self.created_at.strftime("%A, %m%d%Y at %I:%M%p")
  
  @classmethod
  def create_user(cls, username, email, profile_picture_url, password):
    """Creates a new user, hashes the password, stores the new user information in the database, and returns the user."""

    hashed_password = bcrypt.generate_password_hash(password).decode('UTF-8')
    new_user = User(
      username = username,
      email = email,
      profile_picture_url = profile_picture_url,
      password = hashed_password
    )

    db.session.add(new_user)
    return new_user
  
  @classmethod
  def authenticate_user(cls, username, password):
    """Attempts to log in the user. Returns user if successful, returns 0 if user not found in database, returns 1 if password doesn't match."""

    user_logging_in = cls.query.filter_by(username=username).first()

    if user_logging_in:
      do_passwords_match = bcrypt.check_password_hash(user_logging_in.password, password)
      if do_passwords_match:
        return user_logging_in
      return 1
    
    return 0
  
  @classmethod
  def confirm_password(cls, id, password):
    """Make sure the password inputted by the user matches the user's password in the database. Used for submitting forms like updating
    profile info where user must enter password to finalize changes."""

    logged_in_user = cls.query.get(id)

    if logged_in_user:
      return bcrypt.check_password_hash(logged_in_user.password, password)
    return False
  
  @classmethod 
  def update_password(cls, id, new_password):
    """Updates the current logged in user's password and saves it in the database."""

    logged_in_user = cls.query.get(id)
    new_hashed_password = bcrypt.generate_password_hash(new_password).decode('UTF-8')
    logged_in_user.password = new_hashed_password

  # Relationships to link a user with the stories they've uploaded, their favorites, their bookmarks, and their comments.

  stories = db.relationship('Story', cascade='all, delete', backref='user')
  favorites = db.relationship('Favorite', cascade='all, delete', backref='user')
  bookmarks = db.relationship('Bookmark', cascade='all, delete', backref='user')
  comments = db.relationship('Comment', cascade='all, delete', backref='user')

  # Relationships to link a user directly with their favorite stories and bookmarked stories.

  favorite_stories = db.relationship('Story', secondary='favorites', backref='favorite_users')
  bookmarked_stories = db.relationship('Story', secondary='bookmarks', backref='bookmark_users')