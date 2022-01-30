import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from . import db, forms

bp = Blueprint('auth', __name__, url_prefix='/auth')


# REGISTER
@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegistrationForm()

    if request.method == 'POST' and form.validate():
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        db_local = db.get_db()
        error = None

        if not email:
            error = 'Email is required.'
            return jsonify({'status': 'Email is required.'}), 403
        elif not username:
            error = 'Username is required.'
            return jsonify({'status': 'Username is required.'}), 403
        elif not password:
            error = 'Password is required.'
            return jsonify({'status': 'Password is required.'}), 403
        elif not confirm_password:
            error = 'Confirmation password is required.'
            return jsonify({'status': 'Confirmation password is required.'}), 403
        elif password != confirm_password:
            error = "Password and confirmation password don't match."
            return jsonify({'status': "Password and confirmation password don't match."}), 403

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
                return redirect(url_for("auth.login"))

        flash(error, 'danger')

    return render_template('auth/register.html', title='Register', form=form)


# LOGIN
@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    
    if request.method == 'POST' and form.validate():
        error = None

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
            return redirect(url_for('home'))

        flash(error, 'danger')

    return render_template('auth/login.html', title='Login', form=form)


# LOGOUT
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


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