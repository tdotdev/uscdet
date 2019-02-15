from bokeh.sampledata import us_states
from census.dicts import stname_from_code

from bokeh.io import show
from bokeh.layouts import column, widgetbox
from bokeh.models import ColumnDataSource, LogColorMapper, LinearColorMapper
from bokeh.models.widgets import Select
from bokeh.palettes import Viridis11
from bokeh.plotting import figure

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
    
    url = r"https://api.census.gov/data/2014/pep/natstprc?get=STNAME,POP,BIRTHS,DEATHS&DATE=7&for=STATE:*&key=" + API_KEY
    key='STNAME' 
    val_keys=['POP', 'BIRTHS', 'DEATHS']
    """
    url = r"https://api.census.gov/data/2014/pep/natstprc?get=STNAME,DENSITY,DOM,NIM&DATE=7&for=STATE:*&key=" + API_KEY
    key='STNAME' 
    val_keys=['DENSITY', 'DOM', 'NIM']
    """

    IGNORE = ['Puerto Rico Commonwealth', 'District of Columbia']

    geo_data = get_geo_data()
    census_data = get_census_data(url, key=key, vals=val_keys)

    for region in IGNORE:
        census_data.pop(region, None)

    geo_xs = []
    geo_ys =[]
    vals = []
    states = list(census_data.keys())
    val_key = val_keys[0]
    
    for state in census_data:
        geo_xs.append(geo_data[state]['lons'])
        geo_ys.append(geo_data[state]['lats'])
        vals.append(float(census_data[state][val_key]))

    data = ColumnDataSource(dict(
        x=geo_xs,
        y=geo_ys,
        state=states,
        val=vals
    ))

    p = figure(
        title=val_key,
        x_range=(-130,-60),
        y_range=(23, 52),
        plot_width=1200,
        plot_height=675,
        tooltips=[
            ("State", "@state"), (f"Value", "@val")
        ]
    )

    p.grid.grid_line_color = None
    Viridis11.reverse()
    color_mapper = LinearColorMapper(palette=Viridis11)
    p.patches(
        'x', 'y', source=data,
        fill_color={'field':'val', 'transform': color_mapper},
        fill_alpha=.7, line_color="white", line_width=0.5)

    def dataset_select_callback(value, old, new):
        val_key = new
        vals = []
        for state in census_data:
            vals.append(float(census_data[state][val_key]))
        new_data = dict(
            x=geo_xs,
            y=geo_ys,
            state=states,
            val=vals
        )
        data.data = new_data
        p.title.text=val_key

    dataset_select = Select(title='Dataset', value=val_key, options=val_keys)
    dataset_select.on_change('value', dataset_select_callback)

    doc.add_root(column(p, dataset_select))

if __name__ == '__main__':
    pass