from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/geo')
def geo():
    return 'Geographic data endpoint'

@app.route('/chart')
def chart():
    return 'Chart data endpoint.'

@app.route('/tabular')
def tabular():
    return 'Tabular data endpoint.'

@app.route('/novel')
def novel():
    return 'Novel data endpoint.'