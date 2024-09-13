"""This file contains the Story model."""

from models.init_db import db
from datetime import datetime, timezone

class Story(db.Model):
  """Each Story in the app is usually a news article or website that is shared by a user. 
  Each story has a title, optional author (sometimes the author of a story is not quite clear), and a url to the website where 
  users can read the story."""

  __tablename__ = "stories"

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), nullable=False)
  title = db.Column(db.Text, nullable=False)
  author = db.Column(db.Text)
  url = db.Column(db.Text, nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
  updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
