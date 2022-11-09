from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi as MongoServerApi
from pymongo.errors import ConnectionFailure
from pymongo.collection import Collection
from dotenv import dotenv_values
from urllib.parse import quote_plus


class DataStream:
    def __init__(self):
        self.config = dotenv_values(".env")
        self.mongo_user = self.config["MONGO_USER"]
        self.mongo_pass = self.config["MONGO_PASS"]
        self.mongo_host = self.config["MONGO_HOST"]
        self.mongo_uri = f"mongodb://{quote_plus(self.mongo_user)}:{quote_plus(self.mongo_pass)}@{quote_plus(self.mongo_host)}"
        self.mongo_ctx = self.mongo_client()

    def mongo_client(self):
        return MongoClient(self.mongo_uri)

    def mongo_ping(self):
        try:
            self.mongo_ctx.admin.command('ping')
            return True
        except ConnectionFailure:
            return False


class SESApi:
    def __init__(self):
        self.endpoints = {
            "isActiveUser": self.is_active_user,
            "registerUser": self.register_user
        }

    def router(self, endpoint, args):
        if endpoint in self.endpoints.keys():
            return self.endpoints[endpoint](args)
        else:
            return "Endpoint Not Found"

    def is_active_user(self, args):
        print(f'{args}')
        return "IS ACTIVE USER ACTIVATED"

    def register_user(self, args):
        print(f'{args}')
        return 'REGISTER USER ACTIVATED'
