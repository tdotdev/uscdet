from bokeh.sampledata import us_states
from census.dicts import stname_from_code

from bokeh.io import show
from bokeh.models import LogColorMapper, LinearColorMapper
from bokeh.palettes import Viridis11 as palette
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

def geo_plot(url, key, vals):
    IGNORE = ['Puerto Rico Commonwealth', 'District of Columbia']

    geo_data = get_geo_data()
    census_data = get_census_data(url, key='STNAME', vals=['POP', 'DATE'])

    for ign in IGNORE:
        census_data.pop(ign, None)

    for i,w in zip(geo_data, census_data):
        if i != w:
            print(i, w)
    

from census.key import API_KEY
url = r"https://api.census.gov/data/2014/pep/natstprc?get=STNAME,POP&DATE=7&for=STATE:*&key=" + API_KEY
geo_plot(url, key='STNAME', vals=['POP', 'DATE'])