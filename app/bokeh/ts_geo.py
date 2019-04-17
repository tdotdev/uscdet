from bokeh.sampledata import us_states
from census.dicts import FIPS_TO_STNAME, stname_from_code
from census.census_index import c_index
from census.census_data_interface import CensusDataInterface
from app import app

from bokeh.io import show
from bokeh.layouts import column, widgetbox
from bokeh.models import ColumnDataSource, LogColorMapper, LinearColorMapper, ColorBar, BasicTicker
from bokeh.models.widgets import Select, Slider, Button
from bokeh.palettes import Viridis11
from bokeh.plotting import figure, curdoc

from flask import request
import time

"""
api = CensusDataInterface(['pep', 'stchar6'])
geo_data = get_geo_data()
var_params = ['AGE', 'SEX', 'STNAME', 'HISP', 'POP', 'RACE6']
req_params = {'DATE': 7}
all_params = var_params + [key for key in req_params] + ['state']

wanted_params = ['AGE', 'SEX', 'STNAME', 'POP']

with open('census/data/ts.json', 'r') as infile:
    census_data = json.loads(infile.read())


for i, (entry) in enumerate(census_data):
    census_data[i] = {key: entry[all_params.index(key)] for key in wanted_params}

census_data = census_data[1::]
time_series = {}
for entry in census_data:
    state = entry['STNAME']
    if code_from_stname(state):
        key = int(entry['AGE'])
        pop = int(entry['POP'])

        if key not in time_series:
            time_series[key] = {}

        if state in time_series[key]:
            time_series[key][state] += pop
        else:
            time_series[key][state] = pop
"""

def get_geo_data():
    states = us_states.data.copy()
    state_to_geo = {}
    for s in states:
        stname = stname_from_code(s)
        if stname is not None:
            geo_data = states[s]
            state_to_geo[stname] = geo_data
    return {key: state_to_geo[key] for key in sorted(state_to_geo)}

def ts_geo_plot(doc):
    from census.key import API_KEY

    try:
        args = doc.session_context.request.arguments['args'][0].decode(encoding='UTF-8')
    except:
        args = []

    try:
        vargs = doc.session_context.request.arguments['vargs'][0].decode(encoding='UTF-8')
    except:
        vargs = []


    args = eval(args)
    vargs = eval(vargs)

    try:
        cdi = CensusDataInterface(args, vargs)
        census_data = cdi.execute_query()
    except:
        cdi = CensusDataInterface(args)
        census_data = cdi.execute_query()

    

    geo_data = get_geo_data()

    geo_xs = []
    geo_ys =[]
    vals = []
    states = list(census_data.keys())

    list_vars= cdi.get_list_vars()
    list_vars_labels = cdi.get_list_vars_key('label')
    val_keys = {}
    for var, label in zip(list_vars, list_vars_labels):
        val_keys[label] = var

    val_key = list_vars[0]


    for fips in census_data:
        state = FIPS_TO_STNAME[fips]
        geo_xs.append(geo_data[state]['lons'])
        geo_ys.append(geo_data[state]['lats'])
        try:
            vals.append(float(census_data[fips][0][val_key]['val']))
        except:
            vals.append(census_data[fips][0][val_key]['val'])

    times = [time for time in census_data['01']]

    data = ColumnDataSource(dict(
        x=geo_xs,
        y=geo_ys,
        state=[FIPS_TO_STNAME[fips] for fips in states],
        val=vals
    ))

    p = figure(
        title=list_vars_labels[0],
        x_range=(-130,-60),
        y_range=(23, 52),
        plot_width=1200,
        plot_height=675,
        tooltips=[
            ("State", "@state"), (f"Value", "@val")
        ]
    )

    p.grid.grid_line_color = None
    p.xaxis.visible = False
    p.yaxis.visible = False
    p.title.text_font_size = '18pt'

    Viridis11.reverse()
    color_mapper = LinearColorMapper(palette=Viridis11)
    color_bar = ColorBar(color_mapper=color_mapper, ticker=BasicTicker())
    p.add_layout(color_bar, 'right')

    p.patches(
        'x', 'y', source=data,
        fill_color={'field':'val', 'transform': color_mapper},
        fill_alpha=.7, line_color="white", line_width=0.5)

    def dataset_select_callback(value, old, new):
        global val_key
        val_key = val_keys[new]
        vals = []
        
        for fips in census_data:
            try:
                vals.append(float(census_data[fips][0][val_key]['val']))
            except:
                vals.append(census_data[fips][0][val_key]['val'])

        new_data = dict(
            x=geo_xs,
            y=geo_ys,
            state=[FIPS_TO_STNAME[fips] for fips in states],
            val=vals
        )
        data.data = new_data
        p.title.text = new
        time_slider.value = 0


    def time_slider_callback(value, old, new):
        time_index = int(new)
        val_key = val_keys[dataset_select.value]
        vals = []
        for fips in census_data:
            try:
                vals.append(float(census_data[fips][new][val_key]['val']))
            except:
                vals.append(census_data[fips][new][val_key]['val'])

        new_data = dict(
            x=geo_xs,
            y=geo_ys,
            state=states,
            val=vals
        )
        data.data = new_data
            

    def play_button_callback():
        start = time_slider.value
        for i in range(start, 300):
            time_slider.value += 1
            time.sleep(.05)

    time_slider = Slider(start=min(times), end=300, value=min(times), step=1, title='Index')
    time_slider.on_change('value', time_slider_callback)

    play_button = Button(label='Play')
    play_button.on_click(play_button_callback)


    dataset_select = Select(title='Dataset', value=val_key, options=[key for key in val_keys])
    dataset_select.on_change('value', dataset_select_callback)

    doc.add_root(column(p, dataset_select, time_slider, play_button))