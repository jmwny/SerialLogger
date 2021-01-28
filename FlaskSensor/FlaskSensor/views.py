"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from FlaskSensor import app
import sqlite3
from flask import g

DATABASE = r"C:\Users\John\OneDrive\GitHub\SerialLogger\SerialLogger\SensorLog.db"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    #db.row_factory = sqlite3.Row
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    db_vals = query_db('SELECT * FROM env ORDER BY id DESC LIMIT 1')

    ### temps, one hour
    temps = query_db('SELECT tempf FROM env ORDER BY id DESC LIMIT 720')
    tempf = []
    for t in temps:
        tempf.append(float(t[0]))
    tlow = min(tempf)
    thigh = max(tempf)

    ### humidity, one hour
    humidity = query_db('SELECT humidity FROM env ORDER BY id DESC LIMIT 720')
    humidityf = []
    for f in humidity:
        humidityf.append(float(f[0]))
    hlow = min(humidityf)
    hhigh = max(humidityf)

    ### temps, six hours
    temps = query_db('SELECT tempf FROM env ORDER BY id DESC LIMIT 4320')
    tempf = []
    for t in temps:
        tempf.append(float(t[0]))
    tlow2 = min(tempf)
    thigh2 = max(tempf)

    ### humidity, six hours
    humidity = query_db('SELECT humidity FROM env ORDER BY id DESC LIMIT 4320')
    humidityf = []
    for f in humidity:
        humidityf.append(float(f[0]))
    hlow2 = min(humidityf)
    hhigh2 = max(humidityf)

    return render_template(
        'index.html',
        title='Home Page',
        tempc=db_vals[0][1],
        tempf=db_vals[0][2],
        pressure=db_vals[0][3],
        humidity=db_vals[0][4],
        eco2=db_vals[0][5],
        tvoc=db_vals[0][6],
        tlow = tlow,
        thigh = thigh,
        hlow = hlow,
        hhigh = hhigh,
        tlow2 = tlow2,
        thigh2 = thigh2,
        hlow2 = hlow2,
        hhigh2 = hhigh2,
        time=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        year=datetime.now().year
    )
