from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/geo')
def geo():
    return render_template('geo.html')
    
@app.route('/novel')
def novel():
    return render_template('novel.html')

@app.route('/plot')
def chart():
    return render_template('plot.html')

@app.route('/tab')
def tabular():
    return render_template('tab.html')
