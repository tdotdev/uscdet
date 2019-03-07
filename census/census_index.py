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
    
    if d_type == 'timeseries':
        sets = sets[1::]

    entry = c_index.get(d_type, None)

    if entry is None:
        cursor = c_index[d_type] = {}
    else:
        cursor = c_index[d_type]

    for i, (key) in enumerate(sets):
        entry = cursor.get(key, None)
        if i == len(sets) - 1:
            cursor[key] = {'title': title, 'desc': desc}
        else:
            if entry is None:
                cursor[key] = {}
                cursor = cursor[key]
            else:
                cursor = cursor[key]

def entry_to_json(entry, key):
    nodes = []
    
    for new_key in entry[key]:
        if new_key == 'desc' or new_key == 'title':
            nodes.append({'text': entry[key][new_key]})
        else:
            nodes.append(entry_to_json(entry[key], new_key))

    return {'nodes': nodes, 'text': key}

def census_index_json():
    treeview = {
        'text': 'Datasets', 
        'nodes': []
    }
    
    for key in c_index:
        treeview['nodes'].append(entry_to_json(c_index, key))

    ts = [treeview['nodes'][0]]
    nodes = treeview['nodes'][1::]
    treeview['nodes'] = ts + sorted(nodes, key=lambda d: int(d['text']))

    return json.dumps(treeview)