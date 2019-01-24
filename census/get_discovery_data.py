from census_request import *

DATA_DISCOVERY_MAP = {
    'xml': r"https://api.census.gov/data.xml",
    'json': r"https://api.census.gov/data.json"
}

data_dir = os.path.join(os.getcwd(), r"data")
print(f"Writing Data Discover files to {data_dir}")

requests = CensusRequestManager(
    [DATA_DISCOVERY_MAP[key] for key in DATA_DISCOVERY_MAP]
)

requests.request_all()
string_map = requests.parse_all()

for req_url in requests.requests:
    string = string_map[req_url]
    outfile = open(
        os.path.join(data_dir, f"data{requests.requests[req_url].ext}"),
        'w'
    )
    outfile.write(string)
    outfile.close()