import xml.etree.ElementTree as ET
from census.census_request import CensusRequestManager
from census.key import API_KEY
import pickle
import random


def pop_density(doc):
    from bokeh.sampledata import us_states
    us_states = us_states.data.copy()
    l_states = []
    for state in us_states:
        s=us_states[state]
        l_states.append((state,s['lats'],s['lons']))
    l_states.sort(key=lambda tup: tup[0])
    """
    https://api.census.gov/data/{year}/{ds1}/{ds2}/
    """
    url = r"https://api.census.gov/data/2014/pep/natstprc?get=STNAME,POP&DATE=7&for=STATE:*&key=" + API_KEY
    my_requests = CensusRequestManager(url)
    my_requests.request_all()
    z = my_requests.parse_all()
    for key in z:
        data = z[key]
    data = data[1:len(data)-1]
    parts = data.split('\n')
    parsed = []
    for i, (p) in enumerate(parts):
        if i != len(parts) - 1:
            parts[i] = p[:len(p) - 1]
        parsed.append(eval(parts[i]))

    header = parsed[0]
    rows = parsed[1::]

    data = {}
    for i, (r) in enumerate(rows):
        if r[0] == 'Puerto Rico Commonwealth':
            break
        data[l_states[i][0]] = {
            'name': r[0],
            'pop': r[1],
            'lats': l_states[i][1],
            'lons': l_states[i][2]
        }

    from bokeh.models import LogColorMapper, LinearColorMapper
    from bokeh.palettes import Viridis11 as palette
    from bokeh.plotting import figure
    from bokeh.io import show

    palette.reverse()

    country_xs = []
    country_ys = []
    names = []
    population = []
    color_mapper = LinearColorMapper(palette=palette)

    for key in data:
        names.append(key)
        country_xs.append(data[key]['lons'])
        country_ys.append(data[key]['lats'])
        population.append(int(data[key]['pop']))

    data = dict(
        x=country_xs,
        y=country_ys,
        name=names,
        rate=population
    )

    p = figure(
        title="US Population Density, 2014",
        x_range=(-130,-60),
        y_range=(23, 52),
        plot_width=1600,
        plot_height=900
    )
    p.grid.grid_line_color = None
    p.patches(
        'x', 'y', source=data,
        fill_color={'field':'rate', 'transform': color_mapper},
        fill_alpha=.7, line_color="white", line_width=0.5)

    from bokeh.layouts import column
    doc.add_root(column(p))

def pop_density2(doc):
    from bokeh.sampledata import us_states
    us_states = us_states.data.copy()
    l_states = []
    for state in us_states:
        s=us_states[state]
        l_states.append((state,s['lats'],s['lons']))
    l_states.sort(key=lambda tup: tup[0])
    """
    https://api.census.gov/data/{year}/{ds1}/{ds2}/
    """
    url = r"https://api.census.gov/data/2014/pep/natstprc?get=STNAME,POP&DATE=7&for=STATE:*&key=" + API_KEY
    my_requests = CensusRequestManager(url)
    my_requests.request_all()
    z = my_requests.parse_all()
    for key in z:
        data = z[key]
    data = data[1:len(data)-1]
    parts = data.split('\n')
    parsed = []
    for i, (p) in enumerate(parts):
        if i != len(parts) - 1:
            parts[i] = p[:len(p) - 1]
        parsed.append(eval(parts[i]))

    header = parsed[0]
    rows = parsed[1::]

    data = {}
    for i, (r) in enumerate(rows):
        if r[0] == 'Puerto Rico Commonwealth':
            break
        data[l_states[i][0]] = {
            'name': r[0],
            'pop': r[1],
            'lats': l_states[i][1],
            'lons': l_states[i][2]
        }

    from bokeh.models import LogColorMapper, LinearColorMapper
    from bokeh.palettes import Blues9 as palette
    from bokeh.plotting import figure
    from bokeh.io import show

    palette.reverse()

    country_xs = []
    country_ys = []
    names = []
    population = []
    color_mapper = LinearColorMapper(palette=palette)

    for key in data:
        names.append(key)
        country_xs.append(data[key]['lons'])
        country_ys.append(data[key]['lats'])
        population.append(int(data[key]['pop']))

    data = dict(
        x=country_xs,
        y=country_ys,
        name=names,
        rate=population
    )

    p = figure(
        title="US Population Density, 2014",
        x_range=(-130,-60),
        y_range=(23, 52),
        plot_width=1600,
        plot_height=900
    )
    p.grid.grid_line_color = None
    p.patches(
        'x', 'y', source=data,
        fill_color={'field':'rate', 'transform': color_mapper},
        fill_alpha=.7, line_color="white", line_width=0.5)

    from bokeh.layouts import column
    doc.add_root(column(p))

