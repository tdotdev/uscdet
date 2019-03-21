from app import app
from flask import render_template, url_for, request
from bokeh.embed import server_document
from census.census_index import census_index_json


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/query')
def query():
    return render_template('query.html')


@app.route('/geo', methods=['GET'])
def geo():
    args = request.args.getlist('p')
    script = server_document('http://localhost:5006/geo', arguments={'args': args})
    return render_template('geo.html', script=script)

@app.route('/ts_geo', methods=['GET'])
def ts_geo():
    args = request.args.getlist('p')
    script = server_document('http://localhost:5006/ts_geo', arguments={'args': args})
    return render_template('geo.html', script=script)


@app.route('/plot', methods=['GET'])
def plot():
    return render_template('plot.html')

@app.route('/ts_plot', methods=['GET'])
def ts_plot():
    return render_template('plot.html')


@app.route('/index_json')
def index_json():
    return census_index_json()
    

@app.route('/novel')
def novel():
    return render_template('novel')
@app.route('/tab')
def tabular():
    return render_template('tab.html')
