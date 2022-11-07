import unittest
import requests
import urllib.parse
import json

from requests.structures import CaseInsensitiveDict

headers = CaseInsensitiveDict()
headers['Accept'] = 'application/json'
headers['Content-Type'] = 'application/json'

cfg = {
    'url': 'http://localhost:5000/api/post',
    'headers': headers,
    'api_key': '000111000111'
}

class TestApi(unittest.TestCase):
    def test_connection(self):
        url = 'http://localhost:5000/api/post'
        # headers = CaseInsensitiveDict()
        # headers['Accept'] = 'application/json'
        # headers['Content-Type'] = 'application/json'
        data = json.dumps({"api_key": cfg['api_key']})
        response = requests.post(cfg['url'], headers=cfg['headers'], data=data)
        self.assertIs(response.status_code, 200, 'Api Response Should Be 200')

if __name__ == '__main__':
    unittest.main()
