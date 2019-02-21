import json
import os
import pickle
import urllib.request

from census.key import API_KEY

class CensusRequestManager:
    def __init__(self, url=None):
        self.requests = {}
        if url is not None:
            self.add(url)

    def add(self, url):
        self.requests[url] = CensusRequest(url)

    def request_all(self):
        for key in self.requests:
            self.requests[key].request()

    def clear_all(self):
        self.requests.clear()


    def parse_all(self):
        strings = {}
        for key in self.requests:
            strings[key] = self.requests[key].parse()
        
        return strings

class CensusRequest:
    def __init__(self, url):
        self.url = url
        self.response = None

    # Public API
    def parse(self):
        response = self.response.decode('utf8')
        return response
            
    def request(self):
        response = urllib.request.urlopen(self.url)
        self.response = response.read()

    # Private API   
    def get_ext(self):
        exts = ('.xml', '.json')
        ext = os.path.splitext(self.url)[1]
        if ext in exts:
            return ext
        raise ValueError(ext + ' is not a support extensions.')

if __name__ == '__main__':
    print(r"You shouldn't be executing this directly ;-)")