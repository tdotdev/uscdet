from app import app
from flask import render_template
from bokeh.embed import server_document

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/geo')
def geo():
    script = server_document('http://localhost:5006/geo')
    return render_template('geo.html', script=script)
    
@app.route('/novel')
def novel():
    script = server_document('http://localhost:5006/pop_density2')
    return render_template('geo.html', script=script)

@app.route('/plot')
def chart():
    return render_template('plot.html')

@app.route('/tab')
def tabular():
    return render_template('tab.html')
