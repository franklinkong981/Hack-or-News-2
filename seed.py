"""Seed file that will be used throughout development to either insert sample data into the databae or connect to the online Supabase database."""

import os
from app import create_app

from models.init_db import db
from models.user import User
from models.story import Story
from models.favorite import Favorite
from models.bookmark import Bookmark
from models.comment import Comment
from models.connect import connect_db

from dotenv import load_dotenv
load_dotenv()

app = create_app('hackornews2')
# print("The databas is: ", os.environ.get('DATABASE_URL'))
connect_db(app)
app.app_context().push()

# db.session.rollback()

# Create all tables
db.drop_all()
db.create_all()

# If tables aren't empty, empty them
User.query.delete()
Story.query.delete()
Favorite.query.delete()
Bookmark.query.delete()
Comment.query.delete()

db.session.commit()