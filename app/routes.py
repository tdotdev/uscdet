from app import app
from flask import render_template, url_for, request
from bokeh.embed import server_document
from census.census_index import census_index_json
from census.census_data_interface import CensusDataInterface


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

@app.route('/var_select', methods=['GET'])
def var_select():
    args = request.args.getlist('p')
    endpoint = request.args.get('endpoint')
    cdi = CensusDataInterface(args)
    census_vars = {}
    for key in cdi.vars:
        try:
            data = cdi.vars[key]
            label = data['label']
            concept = data['concept']
            dtype = data['predicateType']
            census_vars[key] = {
                'label': label,
                'concept': concept,
                'dtype': dtype
            }
        except:
            pass

    return render_template('var_select.html', args=args, census_vars=census_vars, endpoint=endpoint)


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
