from flask import Blueprint, redirect, url_for
from rasputin.auth import login_required
from . import db

bp = Blueprint('refill', __name__, url_prefix='/refill')

def get_machine_id():
    db_local = db.get_db()
    cursor = db_local.cursor()
    cursor.execute("SELECT id from machine_state")
    return cursor.fetchone()

@bp.route('/coffee')
@login_required
def refill_coffee():
    db_local = db.get_db()
    id = get_machine_id()

    db_local.execute(
        "UPDATE machine_state SET coffee_quantity = ? WHERE id = ?",
        (1000, id)
    )
    db_local.commit()

    return redirect(url_for('home'))

@bp.route('/milk')
@login_required
def refill_milk():
    db_local = db.get_db()
    id = get_machine_id()

    db_local.execute(
        "UPDATE machine_state SET milk_quantity = ? WHERE id = ?",
        (1000, id)
    )
    db_local.commit()

    return redirect(url_for('home'))

@bp.route('/syrup')
@login_required
def refill_syrup():
    db_local = db.get_db()
    id = get_machine_id()

    db_local.execute(
        "UPDATE machine_state SET syrup_quantity = ? WHERE id = ?",
        (100, id)
    )
    db_local.commit()

    return redirect(url_for('home'))

