from tkinter.messagebox import NO
from flask import Blueprint, flash, g, redirect, render_template, request, url_for, current_app, jsonify

from rasputin.auth import login_required
from . import db, forms

bp = Blueprint('profile', __name__, url_prefix='/profile')


# USER PROFILE
@bp.route('/user-profile', methods=('GET', 'POST'))
@login_required
def user_profile():
    with current_app.app_context():
        current_app.config['STATUS_API'] = 'User profile!'
    db_local = db.get_db()
    cursor = db_local.cursor()

    # preference
    cursor.execute("SELECT b.name, p.roast_type, p.syrup FROM user_preference p INNER JOIN beverages_types b ON p.beverage_id = b.id WHERE user_id = ?", (g.user[0],))
    preference = cursor.fetchone()

    # programmed coffees
    cursor.execute("SELECT b.name, p.id, p.roast_type, p.syrup, p.start_time FROM preprogrammed_coffee p INNER JOIN beverages_types b ON p.beverage_id = b.id WHERE user_id = ?", (g.user[0],))
    programmed_coffees = cursor.fetchall()

    form = forms.ProfileForm()
    form.username.data = g.user[1]
    form.birth_date.data = g.user[5]

    context = {'status': None}
    error = None

    if request.method == 'POST':
        username = request.form['username']
        birth_date = request.form['birth_date']

        if username is None:
            error = 'Username required.'
        
        if error is None:
            try:
                db_local.execute(
                    "UPDATE user SET username = ?, birth_date = ? WHERE id = ?",
                    (username, birth_date, g.user[0])
                )
                db_local.commit()
                with current_app.app_context():
                    current_app.config['STATUS_API'] = 'Profile updated successfully!'
                return redirect(url_for('profile.user_profile'))
            except db_local.DatabaseError:
                error = 'Erorr while updating database.'
        with current_app.app_context():
            current_app.config['STATUS_API'] = error
        flash(error, 'danger')

    context['status'] = error
    with current_app.app_context():
        current_app.config['STATUS_API'] = error
    return render_template('profile/profile.html', title='Profile', form=form, preference=preference, programmed_coffees=programmed_coffees, **context)


@bp.route('/api/user-profile', methods=['POST'])
@login_required
def user_profile_api():
    db_local = db.get_db()
    cursor = db_local.cursor()

    # preference
    cursor.execute(
        "SELECT b.name, p.roast_type, p.syrup FROM user_preference p INNER JOIN beverages_types b ON p.beverage_id = b.id WHERE user_id = ?",
        (g.user[0],))
    preference = cursor.fetchone()

    # programmed coffees
    cursor.execute(
        "SELECT b.name, p.id, p.roast_type, p.syrup, p.start_time FROM preprogrammed_coffee p INNER JOIN beverages_types b ON p.beverage_id = b.id WHERE user_id = ?",
        (g.user[0],))
    programmed_coffees = cursor.fetchall()

    error = None

    username = request.form['username']
    birth_date = request.form['birth_date']

    if username is None:
        error = 'Username required.'

    if error is None:
        try:
            db_local.execute(
                "UPDATE user SET username = ?, birth_date = ? WHERE id = ?",
                (username, birth_date, g.user[0])
            )
            db_local.commit()
            return jsonify({
                'status': 'User profile updated successfully',
                'data': {
                    'username': g.user[1],
                    'birth_date': g.user[5]
                }
            }), 200
        except db_local.DatabaseError:
            error = 'Erorr while updating database.'

    return jsonify({
        'status': error,
        'data': {
            'username': g.user[1],
            'birth_date': g.user[5]
        }
    }), 403


# USER PREFERENCE
@bp.route('/preference', methods=('GET', 'POST'))
@login_required
def preference():
    db_local = db.get_db()
    cursor = db_local.cursor()
    cursor.execute("SELECT * FROM user_preference WHERE user_id = ?", (g.user[0],))
    preference = cursor.fetchone()

    cursor.execute("SELECT * FROM beverages_types")
    beverage_list = cursor.fetchall()

    form = forms.PreferenceForm()
    form.beverage_type.choices = [(item[0], item[1]) for item in beverage_list]

    context = {'status': None}
    error = None

    if request.method == 'POST':
        beverage_type = request.form['beverage_type']
        roast_type = request.form['roast_type']
        syrup = True if request.form.get('syrup') else False

        if beverage_type is None:
            error = 'Beverage type is required.'
        if roast_type is None:
            error = 'Roast type is required.'
        with current_app.app_context():
            current_app.config['STATUS_API'] = error
        if preference is not None:
            # deleting previous preference
            try:
                db_local.execute(
                    "DELETE FROM user_preference WHERE id = ?", 
                    (preference[0],)
                )
                with current_app.app_context():
                    current_app.config['STATUS_API'] = 'Preference list updated successfully!'
            except db_local.DatabaseError:
                error = 'Error while deleting from database.'
                with current_app.app_context():
                    current_app.config['STATUS_API'] = error

        try:
            db_local.execute(
                "INSERT INTO user_preference (user_id, beverage_id, roast_type, syrup) VALUES (?, ?, ?, ?)",
                (g.user[0], beverage_type, roast_type, syrup)
            )
            db_local.commit()
            with current_app.app_context():
                current_app.config['STATUS_API'] = 'Preference list updated successfully!'
            return redirect(url_for('profile.user_profile'))
        except db_local.DatabaseError:
            error = 'Error while inserting into database.'
            with current_app.app_context():
                current_app.config['STATUS_API'] = error
    
    context['status'] = error
    with current_app.app_context():
        current_app.config['STATUS_API'] = error
    return render_template('profile/preference-form.html', title='Preference form', form=form, **context)


@bp.route('/api/preference', methods=['POST'])
@login_required
def preference_api():
    db_local = db.get_db()
    cursor = db_local.cursor()
    cursor.execute("SELECT * FROM user_preference WHERE user_id = ?", (g.user[0],))
    preference = cursor.fetchone()

    cursor.execute("SELECT * FROM beverages_types")
    beverage_list = cursor.fetchall()

    error = None

    beverage_type = request.form['beverage_type']
    roast_type = request.form['roast_type']
    syrup = True if request.form.get('syrup') else False

    if beverage_type is None:
        error = 'Beverage type is required.'
    if roast_type is None:
        error = 'Roast type is required.'

    if preference is not None:
        # deleting previsious preferance\
        try:
            db_local.execute(
                "DELETE FROM user_preference WHERE id = ?",
                (preference[0],)
            )
        except db_local.DatabaseError:
            error = 'Error while deleting from database.'

    try:
        db_local.execute(
            "INSERT INTO user_preference (user_id, beverage_id, roast_type, syrup) VALUES (?, ?, ?, ?)",
            (g.user[0], beverage_type, roast_type, syrup)
        )
        db_local.commit()
        return jsonify({
            'status': 'Preference list updated successfully!',
            'data': {
                'username': g.user[1],
                'beverage_type': beverage_type,
                'roast_type': roast_type
            }
        }), 403
    except db_local.DatabaseError:
        error = 'Error while inserting into database.'

    return jsonify({
        'status': error,
        'data': {
            'username': g.user[1],
            'beverage_type': beverage_type,
            'roast_type': roast_type
        }
    }), 403


# USER PROGRAMMED COFFEES
@bp.route('/program', methods=('GET', 'POST'))
@login_required
def program():
    db_local = db.get_db()
    cursor = db_local.cursor()
    cursor.execute("SELECT * FROM beverages_types")
    beverage_list = cursor.fetchall()

    form = forms.ProgrammedCoffeeForm()
    form.beverage_type.choices = [(item[0], item[1]) for item in beverage_list]

    context = {'status': None}
    error = None

    if request.method == 'POST':
        beverage_type = request.form['beverage_type']
        roast_type = request.form['roast_type']
        syrup = True if request.form.get('syrup') else False
        time = request.form['time']

        if beverage_type is None:
            error = 'Beverage type is required.'
        if roast_type is None:
            error = 'Roast type is required.'
        if time is None:
            error = 'Time is required.'
        with current_app.app_context():
            current_app.config['STATUS_API'] = error
        try:
            db_local.execute(
                "INSERT INTO preprogrammed_coffee (user_id, beverage_id, roast_type, syrup, start_time) VALUES (?, ?, ?, ?, ?)",
                (g.user[0], beverage_type, roast_type, syrup, time)
            )
            db_local.commit()
            with current_app.app_context():
                current_app.config['STATUS_API'] = 'Preprogrammed coffee has been successfully saved!'
            return redirect(url_for('profile.user_profile'))
        except db_local.DatabaseError:
            error = 'Error while inserting into database.'
            with current_app.app_context():
                current_app.config['STATUS_API'] = error

    context['status'] = error
    with current_app.app_context():
        current_app.config['STATUS_API'] = error
    return render_template('profile/programmed-coffee-form.html', title='Programmed coffee form', form=form, **context)

@bp.route('/api/program', methods=['POST'])
@login_required
def program_api():
    db_local = db.get_db()
    cursor = db_local.cursor()
    cursor.execute("SELECT * FROM beverages_types")
    beverage_list = cursor.fetchall()

    error = None

    beverage_type = request.form['beverage_type']
    roast_type = request.form['roast_type']
    syrup = True if request.form.get('syrup') else False
    time = request.form['time']

    if beverage_type is None:
        error = 'Beverage type is required.'
    if roast_type is None:
        error = 'Roast type is required.'
    if time is None:
        error = 'Time is required.'

    try:
        db_local.execute(
            "INSERT INTO preprogrammed_coffee (user_id, beverage_id, roast_type, syrup, start_time) VALUES (?, ?, ?, ?, ?)",
            (g.user[0], beverage_type, roast_type, syrup, time)
        )
        db_local.commit()
        return jsonify({
            'status': 'Preprogrammed coffee has been successfully saved!',
            'data': {
                'username': g.user[1],
                'beverage_type': beverage_type,
                'roast_type': roast_type,
                'time': time
            }
        }), 403
    except db_local.DatabaseError:
        error = 'Error while inserting into database.'

    return jsonify({
        'status': error,
        'data': {
            'username': g.user[1],
            'beverage_type': beverage_type,
            'roast_type': roast_type,
            'time': time
        }
    }), 403


@bp.route('/delete-programmed-coffee', methods=('POST', ))
@login_required
def delete_program():
    db_local = db.get_db()
    id = request.form['program_to_delete']

    try:
        db_local.execute(
            "DELETE FROM preprogrammed_coffee WHERE id = ?",
            (id,)
        )
        db_local.commit()
    except db_local.DatabaseError:
        with current_app.app_context():
            current_app.config['STATUS_API'] = 'Could not delete item'
        flash('Could not delete item.', 'danger')
    finally:
        with current_app.app_context():
            current_app.config['STATUS_API'] = 'Item deleted successfully'
        return redirect(url_for('profile.user_profile'))


@bp.route('/api/delete-programmed-coffee', methods=['POST'])
@login_required
def delete_program_api():
    db_local = db.get_db()
    id = request.form['program_to_delete']

    try:
        db_local.execute(
            "DELETE FROM preprogrammed_coffee WHERE id = ?",
            (id,)
        )
        db_local.commit()
    except db_local.DatabaseError:
        return jsonify({
            'status': 'Could not delete item'
        }), 403
    finally:
        return jsonify({
            'status': 'Item deleted successfully'
        }), 200
