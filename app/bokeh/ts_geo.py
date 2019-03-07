import json
import time

from census.census_data_interface import CensusDataInterface
from census.census_request import CensusRequestManager
from app.bokeh.geo import get_geo_data
from census.dicts import *

from bokeh.io import show
from bokeh.layouts import column, widgetbox
from bokeh.models import ColumnDataSource, LogColorMapper, LinearColorMapper
from bokeh.models.widgets import Slider, Button
from bokeh.palettes import Viridis256
from bokeh.plotting import figure
from bokeh.sampledata import us_states

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

def ts_geo_plot(doc):
    
    times = [time for time in time_series]

    geo_xs = []
    geo_ys =[]
    vals = []
    states = [key for key in STNAME_TO_CODE]

    for state in states:
        geo_xs.append(geo_data[state]['lons'])
        geo_ys.append(geo_data[state]['lats'])
        vals.append(time_series[0][state])

    data = ColumnDataSource(dict(
        x=geo_xs,
        y=geo_ys,
        state=states,
        val=vals
    ))

    p_title = "Population by Age"

    p = figure(
        title=p_title,
        x_range=(-130,-60),
        y_range=(23, 52),
        plot_width=1200,
        plot_height=675,
        tooltips=[
            ("State", "@state"), (f"Value", "@val")
        ]
    )


    p.grid.grid_line_color = None
    Viridis256.reverse()
    color_mapper = LinearColorMapper(palette=[z for z in Viridis256 if Viridis256.index(z) % 8 == 0])
    p.patches(
        'x', 'y', source=data,
        fill_color={'field':'val', 'transform': color_mapper},
        fill_alpha=.7, line_color="white", line_width=0.5)

    def time_slider_callback(value, old, new):
        val_key = new
        vals = []
        for state in states:
            vals.append(time_series[val_key][state])

        new_data = dict(
            x=geo_xs,
            y=geo_ys,
            state=states,
            val=vals
        )
        data.data = new_data
        p.title.text=f"{p_title}: {val_key}"

    def play_button_callback():
        start = time_slider.value
        for i in range(start, max(times)):
            time_slider.value += 1
            time.sleep(.05)

    time_slider = Slider(start=min(times), end=max(times), value=min(times), step=1, title='Age')
    time_slider.on_change('value', time_slider_callback)

    play_button = Button(label='Play')
    play_button.on_click(play_button_callback)

    doc.add_root(column(p, time_slider, play_button))