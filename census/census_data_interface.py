import json
import os
from pathlib import Path

from census.census_request import CensusRequestManager
from census.census_index import c_index
from census.key import API_KEY
from census.dicts import FIPS_TO_STNAME


class CensusDataInterface:
    def __init__(self, args, vargs=[]):

        self.args = args
        if args[0] == 'timeseries':
            self.timeseries = True
        else:
            self.timeseries = False

        cursor = c_index
        for arg in self.args:
            cursor = cursor.get(arg, None)

        self.title = cursor['title']
        self.desc = cursor['desc']
        self.var_link = cursor['vars'] + f"?key={API_KEY}"
        self.vars = {}

        crm = CensusRequestManager(self.var_link)
        crm.request_all()

        vars_json = json.loads(crm.parse_all()[self.var_link])
        i = 0
        for vid in vars_json['variables']:
            if len(vargs) == 0:
                if vid != 'for' and vid != 'in' and vid != 'time':
                    var = vars_json['variables'][vid]
                    self.vars[vid] = var
                    i += 1
                    if i == 10:
                        break
            else:
                if vid in vargs:
                    var = vars_json['variables'][vid]
                    self.vars[vid] = var
    
    def print_vars(self):
        print('Vars:')
        for key in self.vars: 
            print(key)

    def get_list_vars(self):
        return [key for key in self.vars]

    def get_list_vars_key(self, meta_key):
        return [self.vars[key][meta_key] for key in self.vars]



    def make_url(self):
        url = f"https://api.census.gov/data"
        for param in self.args:
            url = url + '/' + param

        url = f"{url}?get="

        for key in self.vars:
            url += f"{key},"

        url = url[:-1]

        url += f"&for=STATE:*&key={API_KEY}"

        return url

    def execute_query(self):
        url = self.make_url()
        print('\n\n', url, '\n\n')
        crm = CensusRequestManager(url)
        crm.request_all()
        parsed = crm.parse_all()

        parsed_json = json.loads(parsed[url])
        header = [key for key in parsed_json[0]]
        body = parsed_json[1::]

        header_index = {}
        for i, (key) in enumerate(header):
            header_index[key] = i

        dataset = {}

        if self.timeseries:
            current_key = ''
            time_index = 0
            for entry in body:
                fips_key = entry[header_index['state']]

                if FIPS_TO_STNAME.get(fips_key, None) == None:
                    continue

                if fips_key != current_key:
                    dataset[fips_key] = {}
                    current_key = fips_key
                    time_index = 0

                dataset[fips_key][time_index] = {}

                for key in header_index:
                    if key == 'state':
                        continue
                    var = entry[header_index[key]]
                    dataset[fips_key][time_index][key] = {}
                    dataset[fips_key][time_index][key]['val'] = var
                    dataset[fips_key][time_index][key]['meta'] = self.vars[key]

                time_index += 1
                
        else:
            for entry in body:
                fips_key = entry[header_index['state']]
                if FIPS_TO_STNAME.get(fips_key, None) == None:
                    continue
                dataset[fips_key] = {}
                for key in header_index:
                    if key == 'state':
                        continue
                    var = entry[header_index[key]]
                    dataset[fips_key][key] = {}
                    dataset[fips_key][key]['val'] = var
                    dataset[fips_key][key]['meta'] = self.vars[key]

        return dataset



"""
for switch in range(3):
        
    if switch == 0:
        dset_params = ['pep', 'natstprc']
        var_params = ['STNAME','POP','BIRTHS','DEATHS']
        req_params = {'DATE':7}
    if switch == 1:
        dset_params = ["acs","acs5","subject"]
        var_params = ["S2002_C01_045E","S0103PR_C01_092E"]
        req_params = {}
    if switch == 2:
        dset_params = ['nonemp']
        var_params = ['NAME', 'GEOTYPE']
        req_params = {}

    api = CensusDataInterface(dset_params)
    z = api.build_url_query(var_params, req_params)
    print(z)
"""