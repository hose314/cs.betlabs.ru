import requests


class API:
    __token = ''
    _host = 'http://www.hackerrank.com/x/api/v2/'
    _endpoints = {
        "tests": _host + "tests",
    }
    _default_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    _payload = {
        "access_token": __token
    }
    
    def __init__(self, access_token):
        self.__token = access_token
        self._payload["access_token"] = self.__token
        
    def get_tests(self, test_id=None):
        url = self._endpoints["tests"]

        if test_id is not None:
            url += "/{0}".format(test_id)

        response = requests.get(url, headers=self._default_headers, params=self._payload)
        return response.json()['data']
            
    def get_test_candidates(self, test_id, candidate_id=None):
        if candidate_id is None:
            url = self._endpoints["tests"] + "/{0}/candidates/".format(test_id)
        else:
            url = self._endpoints["tests"] + "/{0}/candidates/{1}".format(test_id, candidate_id)

        response = requests.get(url, headers=self._default_headers, params=self._payload)
        return response.json()['data']
