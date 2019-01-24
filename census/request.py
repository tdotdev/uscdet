import json
import pickle
import urllib.request
import os


class Request:
    def __init__(self, url):
        self.url = url
        self.ext = self.get_ext(url)
        self.response = None

    # Public API
    def parse(self):
        if self.ext == '.json':
            return self.parse_json(self.response)
        elif self.ext == '.xml':
            return self.parse_xml(self.response)
            
    def request(self):
        response = urllib.request.urlopen(self.url)
        self.response = response.read()

    # Private API   
    def get_ext(self, url):
        exts = ('.xml', '.json')
        ext = os.path.splitext(url)[1]
        if ext in exts:
            return ext
        raise ValueError(ext + ' is not a support extensions.')

    def parse_json(self, response):
        decoded = response.decode('utf8')
        return json.loads(decoded)

    def parse_xml(self, response):
        return json.loads(response)


if __name__ == '__main__':
    jurl = r"https://api.census.gov/data.json"
    xurl = r"https://api.census.gov/data.xml"

    req = Request(jurl)
    req.request()
    json = req.parse()
    print(json)
