"""This file contains the Favorites model."""

from models.init_db import db
from datetime import datetime, timezone

class Favorite(db.Model):
  """A User can favorite any Story currently registered in the app, and each Favorite will be associated with a user id and story id."""

  __tablename__ = "favorites"

  user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), primary_key=True)
  story_id = db.Column(db.Integer, db.ForeignKey('stories.id', ondelete='cascade'), primary_key=True)
  created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))