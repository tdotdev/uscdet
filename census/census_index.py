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

print(c_index)