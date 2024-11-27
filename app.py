"""Main application file for the Hack Or News 2 aplication that contains all the imports, routes, and view functions wrapped up in a 
create_app function to create separate instances/application contexts for development and testing."""

import os
from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc

# import forms here

from models.init_db import db
from models.user import User
from models.story import Story
from models.favorite import Favorite
from models.bookmark import Bookmark
from models.comment import Comment
from models.connect import connect_db

"""This key will be in the Flask session and contain the logged in user's id once a user successfully logs in, will be removed once a user
successfully logs out."""
CURRENT_USER_ID = "logged_in_user"

def create_app(db_name, testing=False):
  """Creates an instance of the app to ensure separate production database and testing database, and that sample data inserted into 
  the deatabase for unit/integration testing purposes doesn't interfere with the actual production database."""
  app = Flask(__name__)
  app.testing = testing
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
  # Make sure redirects are followed instead of getting a confirmation page whenever a redirect is initiated.
  app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
  # debugging toolbar used during development process.
  toolbar = DebugToolbarExtension(app)
  if app.testing:
    # Database used for testing is local, not development/production database on Supabase.
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql:///{db_name}'
    # Disable logging tool
    app.config['SQLALCHEMY_ECHO'] = False
    # don't show debug toolbar during testing
    app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
    # bypass CSRF security checking for forms when running tests
    app.config['WTF_CSRF_ENABLED'] = False
  else:
    # Get DB_URI from environ variable (useful for production/testing) or if not set there, set up db locally.
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', f'postgresql:///{db_name}')
    # Logging tool which prints to the terminal any requests sent, errors, etc.
    app.config['SQLALCHEMY_ECHO'] = True
  
  # Routes and view functions for the application.

  ######################################################################################################
  # Functions for user authentication such as signing up, logging in, and logging out.

  @app.before_request
  def store_logged_in_user_to_g_object():
    if CURRENT_USER_ID in session:
      g.user = User.query.get_or_404(session[CURRENT_USER_ID])
    else:
      g.user = None
  
  def add_logged_in_user_to_session(logged_in_user):
    session[CURRENT_USER_ID] = logged_in_user.id

  def remove_logged_out_user_from_session():
    del session[CURRENT_USER_ID]

  ####################################################################################################### 
  # Homepage route
  
  @app.route('/')
  def homepage():
    return render_template("home.html")

  #######################################################################################################
  # Turn off all caching in Flask
  #   (useful for dev; in production, this kind of stuff is typically handled elsewhere.)
  #   Credit to Springboard mentor Jesse B. and Springboard support for directing me to this link:
  #   https://stackoverflow.com/questions/34066804/disabling-caching-in-flask

  @app.after_request
  def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req
  
  return app

app = create_app('hackornews2')
if __name__ == '__main__':
  connect_db(app)
  app.run(debug=True)