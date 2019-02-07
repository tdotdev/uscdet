import xml.etree.ElementTree as ET
from census_request import CensusRequestManager
from key import API_KEY
import pickle


if __name__ == '__main__':

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
    for r in rows:
        data[r[0]] = r[1]


    for key in data:
        print(key, data[key])