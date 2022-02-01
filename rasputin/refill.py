from flask import Blueprint, flash, redirect, url_for, jsonify
from rasputin.auth import login_required
from . import db
from .db import get_db

bp = Blueprint('refill', __name__, url_prefix='/refill')

def get_machine_id():
    db_local = db.get_db()
    cursor = db_local.cursor()
    cursor.execute("SELECT id from machine_state")
    return cursor.fetchone()[0]


# COFFEE REFILL
@bp.route('/coffee')
@login_required
def refill_coffee():
    db_local = db.get_db()
    id = get_machine_id()

    try:
        db_local.execute(
            "UPDATE machine_state SET coffee_quantity = ? WHERE id = ?",
            (1000, id)
        )
        db_local.commit()

        flash('Rasputin is now full on coffee.', 'success')
    except db_local.DatabaseError:
        flash('Error while updating database.', 'danger')
    finally:
        return redirect(url_for('home'))

@bp.route('/api/coffee')
@login_required
def refill_coffee_api():
    db_local = db.get_db()
    id = get_machine_id()
    status = None
    code = 0

    try:
        db_local.execute(
            "UPDATE machine_state SET coffee_quantity = ? WHERE id = ?",
            (1000, id)
        )
        db_local.commit()
        status = 'Rasputin is now full on coffee.'
        code = 200
        flash(status, 'success')
    except db_local.DatabaseError:
        status = 'Error while updating database.'
        code = 403
        flash(status, 'danger')
    finally:
        check = get_db().execute(
            "SELECT coffee_quantity, milk_quantity, syrup_quantity FROM machine_state WHERE id = ?",
            (id,)
        ).fetchone()
        return jsonify({
            'status': status,
            'data': {
                'coffee_quantity': check['coffee_quantity'],
                'milk_quantity': check['milk_quantity'],
                'syrup_quantity': check['syrup_quantity']
            }
        }), code


# MILK REFILL
@bp.route('/milk')
@login_required
def refill_milk():
    db_local = db.get_db()
    id = get_machine_id()

    try:
        db_local.execute(
            "UPDATE machine_state SET milk_quantity = ? WHERE id = ?",
            (1000, id)
        )
        db_local.commit()

        flash('Rasputin is now full on milk.', 'success')
    except db_local.DatabaseError:
        flash('Error while updating database.', 'danger')
    finally:
        return redirect(url_for('home'))

@bp.route('/api/milk')
@login_required
def refill_milk_api():
    db_local = db.get_db()
    id = get_machine_id()
    status = None
    code = 0

    try:
        db_local.execute(
            "UPDATE machine_state SET milk_quantity = ? WHERE id = ?",
            (1000, id)
        )
        db_local.commit()
        status = 'Rasputin is now full on milk.'
        code = 200
        flash(status, 'success')
    except db_local.DatabaseError:
        status = 'Error while updating database.'
        code = 403
        flash(status, 'danger')
    finally:
        check = get_db().execute(
            "SELECT coffee_quantity, milk_quantity, syrup_quantity FROM machine_state WHERE id = ?",
            (id,)
        ).fetchone()
        return jsonify({
            'status': status,
            'data': {
                'coffee_quantity': check['coffee_quantity'],
                'milk_quantity': check['milk_quantity'],
                'syrup_quantity': check['syrup_quantity']
            }
        }), code

# SYRUP REFILL
@bp.route('/syrup')
@login_required
def refill_syrup():
    db_local = db.get_db()
    id = get_machine_id()

    try:
        db_local.execute(
            "UPDATE machine_state SET syrup_quantity = ? WHERE id = ?",
            (100, id)
        )
        db_local.commit()

        flash('Rasputin is now full on syrup.', 'success')
    except db_local.DatabaseError:
        flash('Error while updating database.', 'danger')
    finally:
        return redirect(url_for('home'))

@bp.route('/api/syrup')
@login_required
def refill_syrup_api():
    db_local = db.get_db()
    id = get_machine_id()
    status = None
    code = 0

    try:
        db_local.execute(
            "UPDATE machine_state SET syrup_quantity = ? WHERE id = ?",
            (100, id)
        )
        db_local.commit()
        status = 'Rasputin is now full on syrup.'
        code = 200
        flash(status, 'success')
    except db_local.DatabaseError:
        status = 'Error while updating database.'
        code = 403
        flash(status, 'danger')
    finally:
        check = get_db().execute(
            "SELECT coffee_quantity, milk_quantity, syrup_quantity FROM machine_state WHERE id = ?",
            (id,)
        ).fetchone()
        return jsonify({
            'status': status,
            'data': {
                'coffee_quantity': check['coffee_quantity'],
                'milk_quantity': check['milk_quantity'],
                'syrup_quantity': check['syrup_quantity']
            }
        }), code
