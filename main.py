from rasputin.__init__ import create_app, create_mqtt_app, mqtt, app, thread, socketio
import json

def run_socketio_app():
    app2 = create_app()
    mqtt2, socketio2 = create_mqtt_app(app2)
    socketio2.run(app2, host='localhost', port=5000, use_reloader=False, debug=True)

if __name__ == '__main__':
    run_socketio_app()
