from bokeh.sampledata import us_states
from census.dicts import FIPS_TO_STNAME, stname_from_code
from census.census_index import c_index
from census.census_data_interface import CensusDataInterface
from app import app

from bokeh.io import show
from bokeh.layouts import column, widgetbox
from bokeh.models import ColumnDataSource, LogColorMapper, LinearColorMapper, ColorBar, BasicTicker
from bokeh.models.widgets import Select
from bokeh.palettes import Viridis11
from bokeh.plotting import figure, curdoc

from flask import request

def get_geo_data():
    states = us_states.data.copy()
    state_to_geo = {}
    for s in states:
        stname = stname_from_code(s)
        if stname is not None:
            geo_data = states[s]
            state_to_geo[stname] = geo_data
    return {key: state_to_geo[key] for key in sorted(state_to_geo)}

def get_census_data(url, key, vals):
    from census.census_request import CensusRequestManager

    my_requests = CensusRequestManager(url)
    my_requests.request_all()
    payload = my_requests.parse_all()[url]
    payload = payload.replace('null', 'None')
    parsed = eval(payload)

    data_var_key = parsed[0]
    parsed = parsed[1:]

    assert(key in data_var_key)
    for v in vals:
        assert(v in data_var_key)

    key_i = data_var_key.index(key)
    vals_i = {v: data_var_key.index(v) for v in vals}

    parsed_map = {}

    for entry in parsed:
        value_map = {v: entry[vals_i[v]] for v in vals_i}
        parsed_map[entry[key_i]] = value_map

    return parsed_map

def geo_plot(doc):
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
            vals.append(float(census_data[fips][val_key]['val']))
        except:
            vals.append(census_data[fips][val_key]['val'])

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
        val_key = val_keys[new]
        vals = []
        
        for fips in census_data:
            try:
                vals.append(float(census_data[fips][val_key]['val']))
            except:
                vals.append(census_data[fips][val_key]['val'])

        new_data = dict(
            x=geo_xs,
            y=geo_ys,
            state=[FIPS_TO_STNAME[fips] for fips in states],
            val=vals
        )
        data.data = new_data
        p.title.text = new

    dataset_select = Select(title='Dataset', value=val_key, options=[key for key in val_keys])
    dataset_select.on_change('value', dataset_select_callback)

    doc.add_root(column(p, dataset_select))



if __name__ == '__main__':
    pass