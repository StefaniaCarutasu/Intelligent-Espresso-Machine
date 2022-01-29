from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from . import db, forms

bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/user-profile', methods=('GET', 'POST'))
def show_user():
    db_local = db.get_db()
    cursor = db_local.cursor()

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
            return redirect(url_for('profile.show_user'))
        
        flash(error, 'danger')

    return render_template('profile/profile.html', title='Profile', form=form)



