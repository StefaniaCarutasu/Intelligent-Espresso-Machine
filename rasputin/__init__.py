import os
from threading import Thread

from flask import Flask, request, g, render_template, flash
from flask_mqtt import Mqtt
from flask_socketio import SocketIO

from . import db, auth
from . import forms
from . import refill
from . import suggestion
from . import profile
from . import status

from datetime import datetime
import json
import time
import eventlet

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

        local_db = db.get_db()
        cursor = local_db.cursor()


        # VERIFY MACHINE STATE
        # getting the machine state
        cursor.execute("SELECT * from machine_state")
        current_state = cursor.fetchone()

        if current_state['broken']:
            flash('Rasputin has a technical problem. Please check.', 'danger')
        if current_state['coffee_quantity'] < db.get_min_coffee_val():
            flash('Please, refill the machine with coffee. Is running low.', 'danger')
        if current_state['milk_quantity'] < db.get_min_milk_val():
            flash('Please, refill the machine with milk. Is running low.', 'danger')
        if current_state['syrup_quantity'] < 10:
            flash('Please, refill the machine with syrup. Is running low.', 'danger')


        # MAKE COFFEE FORM
        # getting all beverage types
        cursor.execute("SELECT * FROM beverages_types")
        beverage_list = cursor.fetchall()

        form = forms.CoffeeOptionsForm()
        form.beverage_type.choices = [(item['id'], item['name']) for item in beverage_list]
        

        if request.method == 'POST':
            error = None

            beverage_type = request.form['beverage_type']
            roast_type = request.form['roast_type']
            syrup = True if request.form.get('syrup') else False

            cursor.execute("SELECT * from beverages_types WHERE id = ?", (beverage_type,))
            beverage = cursor.fetchone()

            if beverage['coffee_quantity'] > current_state['coffee_quantity']:
                error = "Not enough coffee in the machine."
            if beverage['milk_quantity'] > current_state['milk_quantity']:
                error = "Not enough milk in the machine."
            if syrup and current_state['syrup_quantity'] < 10:
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

        current_temperature = suggestion.get_temperature()[1]
        if current_temperature:
            current_temperature_celsius = round(current_temperature - 273.15, 2)
            return render_template('home.html', title='Home', temp=current_temperature_celsius, form=form,
                                   preference=preference)
            # return f'Current temperature of {city.title()} is {current_temperature_celsius} &#8451;'
        else:
            error = f"Error getting temperature for {suggestion.get_temperature()[0].title()}"
            flash(error)
            return render_template('home.html', title='Home', form=form, preference=preference)

    @app.route('/status')
    def get_status_api():
        return status.get_status()

    return app

def create_mqtt_app(app):

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

    return mqtt, socketio


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