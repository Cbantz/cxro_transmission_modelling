import requests
import bs4
import urllib
import numpy as np

class Filter:
    URLBASE = 'https://henke.lbl.gov'
    MAX_STEP = 999
    script = "filter.pl"
    def __init__(self):
        pass

    def test_connection(self):
        url = self.URLBASE
        return requests.get(url)

    def _post(self, data):
        url = urllib.request.urljoin(self.URLBASE, '/cgi-bin/' + self.script)
        return requests.post(url, data)
    
    def _retrieve_data(self, response):
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        urldata = soup.body.h2.find('a').attrs['href']

        url = urllib.request.urljoin(self.URLBASE, urldata)
        with urllib.request.urlopen(url) as fp:
            return fp.read()

    def _parse_data(self, s):
        return [list(map(float, line.split())) for line in s.splitlines()[2:]]
    
    def _process(self, data):
        response = self._post(data)
        s = self._retrieve_data(response)
        return self._parse_data(s)
    
    def create_data(self, chemical_formula : str, thickness : float, energy_min : int, energy_max : int, steps : int = 100):
        data = {}
        data['Materia'] = "Enter Formula"
        data['Formula'] = chemical_formula
        data['Density'] = -1
        data['Thickness'] = thickness
        data['Min'] = energy_min
        data['Max'] = energy_max
        data['Npts'] = steps
        data['Plot'] = "Linear"
        data['Output'] = "Plot"
        return data



    def get_transmission(self, chemical_formula : str, thickness : float, energy_min : int, energy_max : int, steps : int = 100):
        data = self.create_data(chemical_formula, thickness, energy_min, energy_max, steps)

        
        return self._process(data)

if __name__=="__main__":
    CXRO_connector = Filter()
    print(CXRO_connector.get_transmission('Si', 5, 30, 2000, 100))
    array = CXRO_connector.get_transmission('Si', 5, 30, 2000, 100)
    for i in array:
        print(i)