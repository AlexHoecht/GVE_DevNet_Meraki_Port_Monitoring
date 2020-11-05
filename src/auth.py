import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from src.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    """
    User registration page
    :return:
    """
    # On user submit
    if request.method == 'POST':
        error = None
        db = get_db()

        # Retrieve Input Forms
        username = request.form['username']
        password = request.form['password']
        apiKey = request.form['apiKey']

        # Check inputs for errors, or if user already exists
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not apiKey:
            error = 'API Key is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        # On Success, commit new user to database
        if error is None:
            db.execute(
                'INSERT INTO user (username, password, accessToken) VALUES (?, ?, ?)',
                (username, generate_password_hash(password), apiKey)
            )
            db.commit()
            return redirect(url_for('auth.login'))

        # Else, Display error
        flash(error)
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    """
    User login page
    :return:
    """
    if request.method == 'POST':
        error = None
        db = get_db()

        # Retrieve Input Forms
        username = request.form['username']
        password = request.form['password']

        # Check if user exists
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        # Check for errors
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        # On Success, Login
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['apiKey'] = user['accessToken']
            return redirect(url_for('dashboard.dashboard'))

        # Else, display error
        flash(error)
    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    """
    Log current user out and clear current session
    :return:
    """
    session.clear()
    return redirect(url_for('auth.login'))


@bp.before_app_request
def load_logged_in_user():
    """
    Retrieve current session user
    :return:
    """
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


def login_required(view):
    """
    Method forcing user login to view page
    :param view:
    :return:
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
