#!/usr/bin/env python3
"""Declare a Flask blueprint to register authentication views.
"""
import functools
import hashlib
import flask
from ratelimit import limits

from db import get_db

THIRTEEN_MINUTES = 1800
bp = flask.Blueprint(  # declare new blueprint
    name='auth',
    import_name=__name__,
    template_folder='templates',
    url_prefix='/auth',
)


@bp.route('/register', methods=('GET', 'POST'))
def register():
    """Register view. Answer a GET request with the registration form.
    Insert new user in db when a POST request occurs and return user to login
    page if everything went right, otherwise to the register view.

    Returns (str): register view or redirect to login page
    """
    if flask.request.method == 'POST':
        username = flask.request.form['username']
        password = flask.request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            # Hash the password using SHA-512
            hashed_password = hashlib.sha512(password.encode()).hexdigest()
            try:
                db.execute(
                    f'INSERT INTO user (username, password) VALUES '
                    f'("{username}", "{hashed_password}")'
                )
                db.commit()
            except db.IntegrityError:  # catch this specific exception
                error = f'User {username} is already registered.'
            else:  # if no exception happened
                return flask.redirect(flask.url_for('auth.login'))

        flask.flash(error, 'error')

    return flask.render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
@limits(calls=10, period = THIRTEEN_MINUTES)
def login():
    """Login view. Answer a GET request with the login form.
    Attach user id if POST request occurs and return user to index
    page if everything went right, otherwise to the login view.

    Returns (str): login view or redirect to index page
    """
    if flask.request.method == 'POST':
        username = flask.request.form['username']
        password = flask.request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            f'SELECT * FROM user WHERE username = "{username}"'
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        else:
            hashed_password = hashlib.sha512(password.encode()).hexdigest()
            if user['password'] != hashed_password:
                error = 'Incorrect password.'

        if error is None:
            # generate redirect response, attach authentication cookie on it
            # and return the response objectTypeError: Expected bytes
            response = flask.redirect(flask.url_for('index'))
            response.set_cookie('user_id', str(user['id']))
            return response

        flask.flash(error, 'error')

    return flask.render_template('auth/login.html')


@bp.route('/logout')
def logout():
    """Clear current user cookie.

    Returns: redirect to index page
    """
    response = flask.redirect(flask.url_for('index'))
    response.delete_cookie('user_id')
    return response


@bp.before_app_request
def load_logged_in_user():
    """If user is currently connected, attach user object to context.
    """
    user_id = flask.request.cookies.get('user_id')

    if user_id is None:
        flask.g.user = None
    else:
        flask.g.user = get_db().execute(
            f'SELECT * FROM user WHERE id = {user_id}'
        ).fetchone()


def login_required(view):
    """Register a view that need authentication. Redirect client to login if
    they are not authenticated.
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if flask.g.user is None:
            return flask.redirect(flask.url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
