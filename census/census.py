import xml.etree.ElementTree as ET
from census_request import CensusRequestManager
from key import API_KEY
import pickle


if __name__ == '__main__':

    """
    https://api.census.gov/data/{year}/{ds1}/{ds2}/
    """
    
    url = r"https://api.census.gov/data/2014/pep/natstprc?get=STNAME,POP&DATE=6&for=state:*&key=" + API_KEY


    my_requests = CensusRequestManager(url)
    my_requests.request_all()
    z = my_requests.parse_all()
    for field in z[url]:
        print(field)