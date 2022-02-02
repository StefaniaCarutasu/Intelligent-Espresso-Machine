import json

from flask import Blueprint, render_template, request, flash, current_app, jsonify
from . import db, forms, __init__
import geocoder
import requests


def get_temperature():
    API_KEY = 'dce1511217da2da880123e2faa59824a'  # initialize your key here
    city = geocoder.ip('me').city.lower()  # city name passed as argument

    # call API and convert response into Python dictionary
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={API_KEY}'
    response = requests.get(url).json()

    # error like unknown city name, inavalid api key
    if response.get('cod') != 200:
        message = response.get('message', '')
        error = f"Error getting temperature for {city.title()}. Error message = {message}"
        flash(error, 'danger')

        context = {'status': error}
        return render_template('home.html', title='Home', **context)

    # get current temperature and convert it into Celsius
    current_temperature = response.get('main', {}).get('temp')
    return city, current_temperature


bp = Blueprint('suggestion', __name__, url_prefix='/suggestion')


def see_suggestions_bloodPressure(systolic, diastolic):
    db_local = db.get_db()

    maxCoffeeLevel = 100
    if systolic > 180 or diastolic > 120:
        maxCoffeeLevel = 0
    elif systolic > 140 or diastolic > 90:
        maxCoffeeLevel = 20
    elif systolic > 120 or diastolic > 80:
        maxCoffeeLevel = 50
        flash('You might want to try decaf coffee', 'success')

    cursor = db_local.cursor()
    cursor.execute(
        "SELECT name, coffee_quantity, milk_quantity FROM beverages_types WHERE 100*coffee_quantity/(milk_quantity+coffee_quantity) <= :coffeeLevel",
        {"coffeeLevel": maxCoffeeLevel})
    tableList = cursor.fetchall()

    return tableList


def see_suggestions_temperature(current_temperature):
    db_local = db.get_db()

    type = 'Hot'
    if (current_temperature > 20):
        type = 'Cold'

    cursor = db_local.cursor()
    cursor.execute("SELECT name, coffee_quantity, milk_quantity FROM beverages_types WHERE coffee_type == :type",
                   {"type": type})
    tableList = cursor.fetchall()

    return tableList


@bp.route('/bloodPressure', methods=('GET', 'POST'))
def search_suggestions_bloodPressure():
    form = forms.BloodPressureForm()
    systolic = 120
    diastolic = 80

    context = {'status': None}
    error = None

    if request.method == 'POST':
        systolic = request.form['systolic'] if request.form['systolic'] else 0
        diastolic = request.form['diastolic'] if request.form['diastolic'] else 0

        if systolic == 0 or diastolic == 0:
            error = 'Introduce your blood pressure.'

    coffeeTypes = see_suggestions_bloodPressure(int(systolic), int(diastolic))
    message = "You might want to try decaf coffee."

    context['status'] = error
    with current_app.app_context():
        current_app.config['STATUS_API'] = 'Coffee suggestions based on blood pressure'
    return render_template('suggestions/bloodPressure.html', title='Login', form=form, coffeeTypes=coffeeTypes,
                           message=message, **context)


@bp.route('/api/bloodPressure', methods=('GET', 'POST'))
def search_suggestions_bloodPressure_api():
    systolic = request.form['systolic']
    diastolic = request.form['diastolic']

    if not systolic or not diastolic:
        status = 'Introduce your blood pressure.'
        return jsonify({'status': status}), 403

    coffeeTypes = see_suggestions_bloodPressure(int(systolic), int(diastolic))
    return json.dumps([dict(coffeeType) for coffeeType in coffeeTypes]), 200


@bp.route('/temperature', methods=('GET', 'POST'))
def search_suggestions_temperature():
    current_temperature = get_temperature()[1]
    current_temperature_celsius = round(current_temperature - 273.15, 2)

    coffeeTypes = see_suggestions_temperature(current_temperature_celsius)
    with current_app.app_context():
        current_app.config['STATUS_API'] = 'Coffee suggestions based on temperature'
    return render_template('suggestions/temperature.html', title='Login', temp=current_temperature_celsius,
                           coffeeTypes=coffeeTypes)


@bp.route('/api/temperature')
def search_suggestions_temperature_api():
    current_temperature = get_temperature()[1]
    current_temperature_celsius = round(current_temperature - 273.15, 2)

    coffeeTypes = see_suggestions_temperature(current_temperature_celsius)
    return json.dumps([dict(coffeeType) for coffeeType in coffeeTypes]), 200
