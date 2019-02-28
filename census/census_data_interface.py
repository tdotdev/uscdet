import json
import os
from pathlib import Path

from census.census_request import CensusRequestManager
from census.key import API_KEY

class CensusDataInterface:
    def __init__(self, dataset_params):
        self.dataset_params = dataset_params

        with open(r"census/data/data.json", 'r') as df:
            data_json = json.loads(df.read())

        for dset in data_json['dataset']:
            if dset['c_dataset'] == dataset_params:
                dataset = dset
                self.year = dset['c_vintage']

        var_link = dataset['c_variablesLink']
        crm = CensusRequestManager(var_link)
        crm.request_all()

        self.opt_vars = {}
        self.req_vars = {}

        vars_json = json.loads(crm.parse_all()[var_link])
        for vid in vars_json['variables']:
            var = vars_json['variables'][vid]
            label = var['label']
            req_var = var.get('required', None)
            if req_var is not None and req_var != 'default displayed':
                self.req_vars[vid] = var
            else:
                self.opt_vars[vid] = var
    
    def print_vars(self):
        print('Required')
        for key in self.req_vars:
            print(key)
        for key in self.opt_vars: 
            print(key)


    def build_url_query(self, var_params, req_params):
        url = f"https://api.census.gov/data/{self.year}"
        for param in self.dataset_params:
            url = url + '/' + param

        url = f"{url}?get="

        for param in var_params:
            url += f"{param},"

        url = url[:-1]

        for param in req_params:
            url += f"&{param}={req_params[param]}"

        url += f"&for=STATE:*&key={API_KEY}"

        return url


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