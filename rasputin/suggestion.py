import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
from . import db, forms

bp = Blueprint('suggestion', __name__, url_prefix='/suggestion')

def see_suggestions(systolic, diastolic):
    error = None

    #if not systolic or not diastolic:
     #   return jsonify({'status': 'Blood pressure is required.'}), 403

    db_local = db.get_db()

    maxCoffeeLevel = 200;
    if systolic > 180 or diastolic > 120:
        maxCoffeeLevel = 0;
    elif systolic > 140 or diastolic > 90:
        maxCoffeeLevel = 70;
    elif systolic > 120 or diastolic > 80:
        maxCoffeeLevel = 100;

    cursor = db_local.cursor()
    cursor.execute("SELECT name, coffee_quantity, milk_quantity FROM beverages_types WHERE coffee_quantity < :coffeeLevel", {"coffeeLevel":maxCoffeeLevel})
    tableList = cursor.fetchall()

    return tableList

@bp.route('/bloodPressure', methods=('GET', 'POST'))
def search_suggestions():
    form = forms.BloodPressureForm()
    systolic = 120
    diastolic = 80
    if request.method == 'POST':
        systolic = request.form['systolic']
        diastolic = request.form['diastolic']


        if systolic is None or diastolic is None:
            error = 'Introduce your blood pressure.'

    coffeeTypes = see_suggestions(int(systolic), int(diastolic))
    return render_template('coffeeSuggestions.html', title='Login', form=form, coffeeTypes = coffeeTypes )