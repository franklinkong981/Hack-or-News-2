"""This file contains the User model."""

from flask_bcrypt import Bcrypt # For user signup/login password hashing

from models.init_db import db
from datetime import datetime, timezone

bcrypt = Bcrypt()

class User(db.Model):
  """User in the app. A user can create an account by putting down a username (50 characters max), unique email, optional profile picture
  url, and password ( at least 8 characters). Once logged in, a user can upload stories."""

  __tablename__ = "users"

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  username = db.Column(db.String(50), nullable=False)
  email = db.Column(db.Text, nullable=False, unique=True)
  profile_picture_url = db.Column(db.Text, default="tbd")
  password = db.Column(db.Text, nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))