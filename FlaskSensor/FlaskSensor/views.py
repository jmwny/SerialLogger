"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from FlaskSensor import app
import sqlite3
from flask import g

DATABASE = r"C:\\Users\\John\\Documents\\GitHub\\SerialLogger\\SerialLogger\\SensorLog.db"

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

    return render_template(
        'index.html',
        title='Home Page',
        tempc=db_vals[0][1],
        tempf=db_vals[0][2],
        pressure=db_vals[0][3],
        humidity=db_vals[0][4],
        eco2=db_vals[0][5],
        tvoc=db_vals[0][6],
        time=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        year=datetime.now().year,
    )
