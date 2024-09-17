"""This file contains the Comments model."""

from models.init_db import db
from datetime import datetime, timezone

class Comment(db.Model):
  """Any user can leave a comment on any story. Each comment has a required content field. Users can create, edit, and delete their own comments."""

  __tablename__ = "comments"

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), primary_key=True)
  story_id = db.Column(db.Integer, db.ForeignKey('stories.id', ondelete='cascade'), primary_key=True)
  content = db.Column(db.Text, nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
  updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))