"""
This script runs the FlaskSensor application using a development server.
"""

from os import environ
from FlaskSensor import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', '192.168.1.50')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
