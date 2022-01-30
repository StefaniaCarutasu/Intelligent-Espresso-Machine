import os
from threading import Thread

from flask import Flask, g, render_template, flash, request
from flask_mqtt import Mqtt
from flask_socketio import SocketIO

from . import db, auth, forms, refill, suggestion, profile, status
import geocoder
import requests
from datetime import datetime
import json
import time
import eventlet
import status

eventlet.monkey_patch()

app=None
thread=None
socketio=None
mqtt=None

def create_app(test_config=None):
    # create and configure the app
    global app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'rasputin.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # initialize db
    db.init_app(app)

    # register auth blueprint
    app.register_blueprint(auth.bp)

    app.register_blueprint(suggestion.bp)
    app.register_blueprint(refill.bp)
    app.register_blueprint(profile.bp)

    # default route
    @app.route('/', methods=('GET', 'POST'))
    def home():
        # TEMPERTATURE API
        global thread
        if thread is None:
            thread = Thread(target=background_thread)
            thread.daemon = True
            thread.start()
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


        # MAKE COFFEE FORM
        # getting all beverage types
        local_db = db.get_db()
        cursor = local_db.cursor()
        cursor.execute("SELECT * FROM beverages_types")
        beverage_list = cursor.fetchall()

        form = forms.CoffeeOptionsForm()
        form.beverage_type.choices = [(item[0], item[1]) for item in beverage_list]
        

        if request.method == 'POST' and form.validate():
            # getting the machine state
            cursor.execute("SELECT * from machine_state")
            current_state = cursor.fetchone()

            error = None

            beverage_type = request.form['beverage_type']
            roast_type = request.form['roast_type']
            syrup = True if request.form.get('syrup') else False

            cursor.execute("SELECT * from beverages_types WHERE id = ?", (beverage_type,))
            beverage = cursor.fetchone()

            if beverage[2] > current_state[1]:
                error = "Not enough coffee in the machine."
            if beverage[3] > current_state[2]:
                error = "Not enough milk in the machine."
            if syrup and current_state[3] < 10:
                error = "Not enough syrup in the machine."
            
            if error is None:
                flash('Rasputin is working on your coffee...', 'success')
                local_db.execute(
                    "UPDATE machine_state SET coffee_quantity = ?, milk_quantity = ?, syrup_quantity = ? WHERE id  = ?",
                    (current_state[1] - beverage[2], current_state[2] - beverage[3], current_state[3] - (10 if syrup else 0), current_state[0])
                )
                local_db.commit()
            else:
                flash(error, 'danger')


        preference = False
        if g.user:
            # USER PREFERERENCE
            cursor.execute("SELECT id FROM user_preference WHERE user_id = ?", (g.user[0],))
            preference = True if cursor.fetchone() else False

            # PROGRAMMED COFFEES
            current_time = datetime.now().strftime("%H:%M")
            cursor.execute("SELECT id FROM preprogrammed_coffee WHERE user_id = ? AND start_time = ?", (g.user[0], current_time))

            if cursor.fetchone():
                flash('Rasputin is working on programmed coffee...', 'success')


        if current_temperature:
            current_temperature_celsius = round(current_temperature - 273.15, 2)
            return render_template('home.html', title='Home', temp=current_temperature_celsius, form=form, preference=preference)
            # return f'Current temperature of {city.title()} is {current_temperature_celsius} &#8451;'
        else:
            error = f"Error getting temperature for {city.title()}"
            flash(error)
            return render_template('home.html', title='Home', form=form, preference=preference)

    return app

def create_mqtt_app():

    # Setup connection to mqtt broker
    app.config['MQTT_BROKER_URL'] = 'localhost'  # use the free broker from HIVEMQ
    app.config['MQTT_BROKER_PORT'] = 1883  # default port for non-tls connection
    app.config['MQTT_USERNAME'] = ''  # set the username here if you need authentication for the broker
    app.config['MQTT_PASSWORD'] = ''  # set the password here if the broker demands authentication
    app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
    app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes

    global mqtt
    mqtt = Mqtt(app)
    global socketio
    socketio = SocketIO(app, async_mode="eventlet")

    return mqtt


def background_thread():
    count = 0
    while True:
        time.sleep(1)
        # Using app context is required because the get_status() functions
        # requires access to the db.
        with app.app_context():
            message = json.dumps(status.get_status(), default=str)
        # Publish
        mqtt.publish('python/mqtt', message)