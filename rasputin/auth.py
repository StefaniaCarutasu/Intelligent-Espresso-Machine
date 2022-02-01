import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from . import db, forms

bp = Blueprint('auth', __name__, url_prefix='/auth')


# REGISTER
@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegistrationForm()
    context = {'status': None}
    error = None

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        db_local = db.get_db()

        if not email:
            error = 'Email is required.'
        elif not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not confirm_password:
            error = 'Confirmation password is required.'
        elif password != confirm_password:
            error = "Password and confirmation password don't match."

        if error is None:
            try:
                db_local.execute(
                    "INSERT INTO user (username, email, password) VALUES (?, ?, ?)",
                    (username, email, generate_password_hash(password)),
                )
                db_local.commit()
            except db_local.IntegrityError:
                error = f"User {username} is already registered."
            else:
                flash(f'Account created for {form.username.data}!', 'success')
                with current_app.app_context():
                    current_app.config['STATUS_API'] = 'Account created successfully!'
                return redirect(url_for("auth.login"))

        flash(error, 'danger')

    context['status'] = error
    with current_app.app_context():
        current_app.config['STATUS_API'] = error
    return render_template('auth/register.html', title='Register', form=form, **context)

@bp.route('/api/register', methods=['POST'])
def register_api():
    error = None

    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    db_local = db.get_db()

    if not email:
        error = 'Email is required.'
    elif not username:
        error = 'Username is required.'
    elif not password:
        error = 'Password is required.'
    elif not confirm_password:
        error = 'Confirmation password is required.'
    elif password != confirm_password:
        error = "Password and confirmation password don't match."

    if error is None:
        try:
            db_local.execute(
                "INSERT INTO user (username, email, password) VALUES (?, ?, ?)",
                (username, email, generate_password_hash(password)),
            )
            db_local.commit()
        except db_local.IntegrityError:
            error = f"User {username} is already registered."
        else:
            return jsonify({'status': 'Account created succesfully!'}), 200

    return jsonify({'status': error}), 403


# LOGIN
@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    context = {'status': None}
    error = None
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # remeber = request.form['remeber']
        db_local = db.get_db()

        user = db_local.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            flash('You have been logged in!', 'success')
            with current_app.app_context():
                current_app.config['STATUS_API'] = 'Log in succesful!'
            return redirect(url_for('home'))

        flash(error, 'danger')

    context['status'] = error
    with current_app.app_context():
        current_app.config['STATUS_API'] = error
    return render_template('auth/login.html', title='Login', form=form, **context)


@bp.route('/api/login', methods=['POST'])
def login_api():
    error = None

    username = request.form['username']
    password = request.form['password']
    db_local = db.get_db()

    user = db_local.execute(
        'SELECT * FROM user WHERE username = ?', (username,)
    ).fetchone()

    if user is None:
        error = 'Incorrect username.'
    elif not check_password_hash(user['password'], password):
        error = 'Incorrect password.'

    if error is None:
        session.clear()
        session['user_id'] = user['id']
        return jsonify({'status': 'Logged in succesfully!'}), 200

    return jsonify({'status': error}), 403


# LOGOUT
@bp.route('/logout')
def logout():
    session.clear()
    with current_app.app_context():
        current_app.config['STATUS_API'] = 'Log out successful!'
    return redirect(url_for('home'))

@bp.route('/api/logout')
def logout_api():
    session.clear()
    return jsonify({'status': 'Logged out successfully!'}), 200


# decorator for checking if a user is loaded
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        # redirecting to login page if no user is already logged in
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

# selecting current user before any view is shown
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db.get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()