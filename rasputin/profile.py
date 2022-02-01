from tkinter.messagebox import NO
from flask import Blueprint, flash, g, redirect, render_template, request, url_for


from rasputin.auth import login_required
from . import db, forms

bp = Blueprint('profile', __name__, url_prefix='/profile')


# USER PROFILE
@bp.route('/user-profile', methods=('GET', 'POST'))
@login_required
def user_profile():
    db_local = db.get_db()
    cursor = db_local.cursor()

    # prference
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

        if not username:
            error = 'Username required.'
        
        if error is None:
            try:
                db_local.execute(
                    "UPDATE user SET username = ?, birth_date = ? WHERE id = ?",
                    (username, birth_date, g.user[0])
                )
                db_local.commit()
                
                return redirect(url_for('profile.user_profile'))
            except db_local.DatabaseError:
                error = 'Erorr while updating database.'
            
        flash(error, 'danger')

    context['status'] = error
    return render_template('profile/profile.html', title='Profile', form=form, preference=preference, programmed_coffees=programmed_coffees, **context)


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

        if not beverage_type:
            error = 'Beverage type is required.'
        if not roast_type:
            error = 'Roast type is required.'

        context['status'] = error

        if error is None:
            if preference is not None:
                # deleting previsious preferance\
                try:
                    db_local.execute(
                        "DELETE FROM user_preference WHERE id = ?",
                        (preference[0],)
                    )
                except db_local.DatabaseError:
                    error = 'Error while deleting from database.'
                    context['status'] = error

            try:
                db_local.execute(
                    "INSERT INTO user_preference (user_id, beverage_id, roast_type, syrup) VALUES (?, ?, ?, ?)",
                    (g.user[0], beverage_type, roast_type, syrup)
                )
                db_local.commit()

                return redirect(url_for('profile.user_profile'))
            except db_local.DatabaseError:
                error = 'Error while inserting into database.'
    
                context['status'] = error


    return render_template('profile/preference-form.html', title='Preference form', form=form, **context)


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

    error = None
    context = {'status': None}


    if request.method == 'POST':
        beverage_type = request.form['beverage_type']
        roast_type = request.form['roast_type']
        syrup = True if request.form.get('syrup') else False
        time = request.form['time']

        if not beverage_type:
            error = 'Beverage type is required.'
        if not roast_type:
            error = 'Roast type is required.'
        if not time:
            error = 'Time is required.'

        context['status'] = error

        if error is None:
            try:
                db_local.execute(
                    "INSERT INTO preprogrammed_coffee (user_id, beverage_id, roast_type, syrup, start_time) VALUES (?, ?, ?, ?, ?)",
                    (g.user[0], beverage_type, roast_type, syrup, time)
                )
                db_local.commit()

                return redirect(url_for('profile.user_profile'))
            except db_local.DatabaseError:
                error = 'Error while inserting into database.'

                context['status'] = error

    return render_template('profile/programmed-coffee-form.html', title='Programmed coffee form', form=form, **context)

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
        flash('Could not delete item.', 'danger')
    finally:
        return redirect(url_for('profile.user_profile'))
