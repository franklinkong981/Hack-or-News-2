"""This file contains the Bookmarks model."""

from models.init_db import db
from datetime import datetime, timezone

class Bookmark(db.Model):
  """A User can bookmark any Story in the app. Each bookmark has an associated user id and story id."""

  __tablename__ = "bookmarks"

  user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), primary_key=True)
  story_id = db.Column(db.Integer, db.ForeignKey('stories.id', ondelete='cascade'), primary_key=True)
  created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))