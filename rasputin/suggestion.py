from flask import Blueprint, render_template, request, flash
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
        flash(error)
        return render_template('home.html', title='Home')

    # get current temperature and convert it into Celsius
    current_temperature = response.get('main', {}).get('temp')
    return city, current_temperature


bp = Blueprint('suggestion', __name__, url_prefix='/suggestion')

def see_suggestions_bloodPressure(systolic, diastolic):
    error = None

    #if not systolic or not diastolic:
     #   return jsonify({'status': 'Blood pressure is required.'}), 403

    db_local = db.get_db()

    maxCoffeeLevel = 100;
    if systolic > 180 or diastolic > 120:
        maxCoffeeLevel = 0;
    elif systolic > 140 or diastolic > 90:
        maxCoffeeLevel = 20;
    elif systolic > 120 or diastolic > 80:
        maxCoffeeLevel = 50;
        flash('You might want to try decaf coffee', 'success')

    cursor = db_local.cursor()
    cursor.execute("SELECT name, coffee_quantity, milk_quantity FROM beverages_types WHERE 100*coffee_quantity/(milk_quantity+coffee_quantity) <= :coffeeLevel", {"coffeeLevel":maxCoffeeLevel})
    tableList = cursor.fetchall()

    return tableList

def see_suggestions_temperature(current_temperature):
    error = None

    #if not systolic or not diastolic:
     #   return jsonify({'status': 'Blood pressure is required.'}), 403

    db_local = db.get_db()

    type = 'Hot'
    if(current_temperature > 20):
        type = 'Cold'

    cursor = db_local.cursor()
    cursor.execute("SELECT name, coffee_quantity, milk_quantity FROM beverages_types WHERE coffee_type == :type", {"type":type})
    tableList = cursor.fetchall()

    return tableList


@bp.route('/bloodPressure', methods=('GET', 'POST'))
def search_suggestions_bloodPressure():
    form = forms.BloodPressureForm()
    systolic = 120
    diastolic = 80
    if request.method == 'POST':
        systolic = int(request.form['systolic'])
        diastolic = int(request.form['diastolic'])


        if systolic is None or diastolic is None:
            error = 'Introduce your blood pressure.'


    coffeeTypes = see_suggestions_bloodPressure(int(systolic), int(diastolic))
    message = "You might want to try decaf coffee."
    return render_template('suggestions/bloodPressure.html', title='Login', form=form, coffeeTypes = coffeeTypes, message = message)

@bp.route('/temperature', methods=('GET', 'POST'))
def search_suggestions_temperature():

    current_temperature = get_temperature()[1]
    current_temperature_celsius = round(current_temperature - 273.15, 2)

    coffeeTypes = see_suggestions_temperature(current_temperature_celsius)
    return render_template('suggestions/temperature.html', title='Login', temp = current_temperature_celsius, coffeeTypes = coffeeTypes )