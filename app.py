"""Main application file for the Hack Or News 2 aplication that contains all the imports, routes, and view functions wrapped up in a 
create_app function to create separate instances/application contexts for development and testing."""

import os
from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc

# import forms here
from forms.authenticate_forms import SignupForm, LoginForm

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
  
  @app.route('/signup', methods=['GET', 'POST'])
  def handle_signup():
    """GET: display user signup form.
    POST Success: Create new User instance, add new user to database, redirect user to login form.
    POST fail: Redirect to signup form with error message. """

    if g.user:
      flash("You already have an account and are signed in", "danger")
      return redirect('/')
    
    signup_form = SignupForm()

    if signup_form.validate_on_submit():
      try:
        new_user = User.create_user(
          username = signup_form.username.data,
          email = signup_form.email.data,
          profile_picture_url = signup_form.profile_picture_url.data or User.profile_picture_url.default.arg,
          password = signup_form.password.data
        )
        db.session.commit()

        flash("Account successfully created. Please log in", "success")
        return redirect('/login')
      except IntegrityError as exc:
        # Only possible error not covered by WTForms validation is email/username isn't unique. Inspect error message to see which one it is.
        # exic.orig gives the error message of the error, and repr converts it into a string.
        if "username" in repr(exc.orig):
          flash(f"There is already an account associated with the username {signup_form.username.data}", "danger")
        elif "email" in repr(exc.orig):
          flash(f"There is already an account associated with the email {signup_form.email.data}", "danger")
        else:
          flash("Something went wrong with the database in the signup process. Please try again later", "danger")
        print(f"ERROR: {exc}")
      except Exception as exc:
        # Internal issue.
        flash("There was an internal server error. Please try again later.", "danger")
        print(f"ERROR: {exc}")
    
    return render_template('users/signup.html', form=signup_form)
  
  @app.route('/login', methods=['GET', 'POST'])
  def handle_login():
    """GET: dsplay user login form.
    POST Success: Redirect to signed in homepage.
    POST fail: Redirect to login form with error message."""

    if g.user:
      flash("You already have an account and are logged in", "danger")
      return redirect("/")
    
    login_form = LoginForm()

    if login_form.validate_on_submit():
      try:
        user_logging_in = User.authenticate_user(login_form.username.data, login_form.password.data)

        # User.authenticate_user returns 0 if username isn't found in database, 1 if passwords don't match.
        if user_logging_in != 0 and user_logging_in != 1:
          add_logged_in_user_to_session(user_logging_in)
          flash(f"Hello, {user_logging_in.username}!", "success")
          return redirect("/")
        elif user_logging_in == 0:
          flash("The username you entered is not associated with any account", "danger")
        elif user_logging_in == 1:
          flash("The password you entered is incorrect", "danger")
        
      except Exception as exc:
        # Internal issue.
        flash("There was an internal server error. Please try again later.", "danger")
        print(f"ERROR: {exc}")

    return render_template('users/login.html', form=login_form)
  
  @app.route('/logout')
  def handle_logout():
    if not g.user:
      flash("You are already signed out", "danger")
    else:
      remove_logged_out_user_from_session()
      flash("Successfully logged out.", "success")
    
    return redirect("/")

  ######################################################################################################

  # Homepage route
  @app.route('/')
  def homepage():
    if g.user:
      return render_template("logged-in-home.html")
    else:
      return render_template("logged-out-home.html")

  #######################################################################################################
  # 404 Page Not Found Error Handler

  @app.errorhandler(404)
  def page_not_found(e):
    flash("404 Not Found: The URL you requested was not found", "danger")

    return redirect("/")

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