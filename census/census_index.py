import json

with open(r"census/data/data.json", 'r') as df:
    data_json = json.loads(df.read())

c_index = {
    'timeseries': {}
}

for dset in data_json['dataset']:
    d_type = dset.get('c_vintage', 'timeseries')
    sets = dset['c_dataset']
    title = dset['title']
    desc = dset['description']
    variables = dset['c_variablesLink']
    groups = dset['c_groupsLink']
    
    if d_type == 'timeseries':
        sets = sets[1::]
    else:
        d_type = str(d_type)

    entry = c_index.get(d_type, None)

    if entry is None:
        cursor = c_index[d_type] = {}
    else:
        cursor = c_index[d_type]

    for i, (key) in enumerate(sets):
        entry = cursor.get(key, None)
        if i == len(sets) - 1:
            cursor[key] = {'title': title, 'desc': desc, 'vars': variables, 'groups': groups}
        else:
            if entry is None:
                cursor[key] = {}
                cursor = cursor[key]
            else:
                cursor = cursor[key]

def entry_to_json(entry, key):
    nodes = []
    IGNORE = ['selectable', 'tags', 'icon', 'backColor', 'vars', 'groups']
    for new_key in entry[key]:
        if new_key in IGNORE:
            continue
        if new_key == 'title':
            nodes.append({'text': f"{entry[key][new_key]}", 'backColor': '#d1ffe9'})
        elif new_key == 'desc':
            nodes.append({
                'text': 'Description', 
                'backColor': '#edfff6',
                'selectable': False, 
                'nodes': [{
                    'text': entry[key][new_key],
                    'selectable': False
                }]
            })
        else:
            nodes.append(entry_to_json(entry[key], new_key))

    return {'nodes': nodes, 'text': key, 'selectable': False}

def census_index_json():
    treeview = {
        'text': 'Datasets', 
        'nodes': [],
        'selectable': False,
        'state': {
            'expanded': False
        }
    }
    
    for key in c_index:
        treeview['nodes'].append(entry_to_json(c_index, key))

    ts = treeview['nodes'][0]
    ts['text'] = 'Time Series'
    nodes = treeview['nodes'][1::]
    non_ts = {
        'text': 'Non Time Series',
        'selectable': False,
        'nodes': sorted(nodes, key=lambda d: int(d['text']))
    }
    treeview['nodes'] = [ts] + [non_ts]

    return json.dumps(treeview)