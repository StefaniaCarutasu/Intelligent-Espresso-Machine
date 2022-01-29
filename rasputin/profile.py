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
    cursor.execute("SELECT * FROM user_preference WHERE user_id = ?", (g.user[0],))
    preference = cursor.fetchone()

    # programmed coffees
    cursor.execute("SELECT * FROM preprogrammed_coffee WHERE user_id = ?", (g.user[0],))
    programmed_coffees = cursor.fetcall()

    form = forms.ProfileForm()
    form.username.data = g.user[1]
    form.birth_date.data = g.user[5]

    if request.method == 'POST' and form.validate():
        error = None

        username = request.form['username']
        birth_date = request.form['birth_date']

        if username is None:
            error = 'Username required.'
        
        if error is None:
            db_local.execute(
                "UPDATE user SET username = ?, birth_date = ? WHERE id = ?",
                (username, birth_date, g.user[0])
            )
            db_local.commit()
            return redirect(url_for('profile.user_profile'))
        
        flash(error, 'danger')

    return render_template('profile.html', title='Profile', form=form, prference=preference, programmed_coffees=programmed_coffees)


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

    form = forms.CoffeeOptionsForm()
    form.beverage_type.choices = [(item[0], item[1]) for item in beverage_list]
    form.submit.name = "Set preference"

    if request.method == 'POST' and form.validate():
        beverage_type = request.form['beverage_type']
        roast_type = request.form['roast_type']
        syrup = True if request.form.get('syrup') else False

        if preference is not None:
            # deleting previsious preferance
            db_local.execute(
                "DELETE FROM user_preferece WHERE user_id = ?", 
                (g.user[0])
            )

        db_local.execute(
            "INSERT INTO user_preference (user_id, beverage_id, roast_type, syrup) VALUES (?, ?, ?, ?)",
            (g.user[0], beverage_type, roast_type, syrup)
        )
        db_local.commit()

        return redirect(url_for('profile.user_profile'))

