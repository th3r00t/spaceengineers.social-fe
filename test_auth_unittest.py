import json
import subprocess
import time
import unittest

import requests
from requests.structures import CaseInsensitiveDict

from sesocial.sesapi import DataStream

headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"
headers["Content-Type"] = "application/json"

cfg = {
    "url": "http://localhost:5000/api/post",
    "headers": headers,
    "api_key": "000111000111",
    "flask_pid": 0,
}


class TestApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        command = "python -m flask --debug run"
        _proc = subprocess.Popen(command, shell=True)
        cfg["flask_pid"] = _proc.pid
        time.sleep(2.5)

    @classmethod
    def tearDownClass(cls):
        command = f"kill -9 {cfg['flask_pid'].__str__()}"
        subprocess.call(command, shell=True)

    def test_connection(self):
        data = json.dumps({"api_key": cfg["api_key"]})
        response = requests.post(cfg["url"], headers=cfg["headers"], data=data)
        self.assertIs(response.status_code, 200, "Api Response Should Be 200")

    def test_endpoints(self):
        endpoints = ["isUser", "registerUser"]
        args = {"steam64id": 1010100010, "username": "testuser"}
        for _ep in endpoints:
            data = json.dumps(
                {"api_key": cfg["api_key"], "endpoint": _ep, "args": args}
            )
            response = requests.post(cfg["url"], headers=cfg["headers"], data=data)
            print(response.content)
            self.assertIs(response.status_code, 200, f"{_ep} Endpoint Failure")

    def test_mongo_ctx(self):
        _ds = DataStream()
        self.assertTrue(_ds.mongo_ping(), "Failed Mongo Connection")


if __name__ == "__main__":
    unittest.main()
