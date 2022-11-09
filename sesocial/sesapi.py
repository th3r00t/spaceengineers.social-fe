"""Api Definitions for spaceengineers.social."""
from datetime import datetime
from urllib.parse import quote_plus

from dotenv import dotenv_values
from markupsafe import escape
from pymongo.errors import ConnectionFailure
from pymongo.mongo_client import MongoClient


class DataStream:
    """Establishes connection to MongoDb."""

    def __init__(self):
        """Initialize required settings for database connections."""
        self.config = dotenv_values(".env")
        self.mongo_user = self.config["MONGO_USER"]
        self.mongo_pass = self.config["MONGO_PASS"]
        self.mongo_host = self.config["MONGO_HOST"]
        self.mongo_uri = f"mongodb://{quote_plus(self.mongo_user)}:{quote_plus(self.mongo_pass)}@{quote_plus(self.mongo_host)}"
        self.mongo_ctx = self.mongo_client()
        self.db = self.mongo_ctx.sesocial

    def mongo_client(self):
        """Return mongodb client object."""
        return MongoClient(self.mongo_uri)

    def mongo_ping(self):
        """Check for established connection to mongodb."""
        try:
            self.mongo_ctx.admin.command("ping")
            return True
        except ConnectionFailure:
            return False


class SESApi:
    """Holds all main functions related to api calls.

    Attributes
    ----------
    endpoints: dict
        {'endpoint': function}
    msg_preamle: string
    warn_preamble: string
    error_preamble: string

    Methods
    ----------
    router(endpoint, args)
        routes api calls.
    check_args(args, expected)
        checks for required args.
    is_user(args)
        :noindex:
        internal user check method.
    is_active_user(args)
        Endpoint handler.
    register_user(args)
        Endpoint handler.
    """

    def __init__(self):
        """Initialize api specific variables."""
        self.endpoints = {"isUser": self.is_user, "registerUser": self.register_user}
        self.msg_preamble = escape("ses >   ")
        self.warn_preamble = escape("ses !>  ")
        self.error_preamble = escape("ses !!> ")

    def router(self, endpoint, args):
        """Routes api calls.

        Parameters
        ----------
        endpoint : str
            desired api endpoint
        args: array, optional
            KeyValue dictionary: example [{"steam64id": 11001001010, "username": 'exampleUser'}]
        Returns
        ----------
        route results: json
        failure package: json
        """
        if endpoint in self.endpoints.keys():
            return self.endpoints[endpoint](args)
        else:
            try:
                return {
                    "success": False,
                    "msg": f"{self.warn_preamble}{endpoint} not found.",
                }
            except KeyError as ke:
                return {
                    "success": False,
                    "msg": f"{self.error_preamble}no endpoint specified.",
                    "error": ke,
                }

    def check_args(self, args, expected):
        """Check whether the arguments required by the requested endpoint have been provided.

        Parameters
        ----------
        args: array
            Key Value dicts provided by the originating call
        expected: array
            arguments required by requested endpoint
        Returns
        ----------
        True: requested arguments found
        False: requested arguments not found
        """
        for arg in expected:
            if arg in args.keys():
                continue
            else:
                return False
        return True

    def is_user(self, args):
        """Endpoint: checks database for user by steam64id.

        Parameters
        ----------
        args: array, required
            {'steam64id': int, 'username': string}
        Returns
        ----------
        json: {'success': bool, 'msg': string}
        """
        _db = DataStream().db
        expected = ["steam64id", "username"]
        if self.check_args(args, expected):
            if _db.users.find_one({"steam64id": args["steam64id"]}):
                return {
                    "success": True,
                    "msg": f"{self.msg_preamble}found user with steam64id {args['steam64id']}.",
                }
            else:
                return {
                    "success": False,
                    "msg": f"{self.warn_preamble}no user with steam64id {args['steam64id']} found.",
                }

    def is_active_user(self, args):
        """Internaly check if user is already present.

        Parameters
        ----------
        args: array, required
            {'steam64id': int, 'username': string}
        Returns
        ----------
        bool
        """
        _db = DataStream().db
        expected = ["steam64id", "username"]
        if self.check_args(args, expected):
            if _db.users.find_one({"steam64id": args["steam64id"]}):
                return True
            else:
                return False

    def register_user(self, args):
        """Endpoint: registers user by steam64id.

        Implements internal is_active_user call

        Parameters
        ----------
        args: array, required
            {'steam64id': int, 'username': string}
        Returns
        ----------
        json: {'success': bool, 'msg': string}
        """
        _db = DataStream().db
        expected = ["steam64id", "username"]
        if self.check_args(args, expected):
            if not self.is_active_user(args):
                _op = _db.users.insert_one(
                    {
                        "steam64id": args["steam64id"],
                        "username": args["username"],
                        "creation": datetime.now(),
                    }
                )
                return {
                    "success": True,
                    "msg": f"{self.msg_preamble}registered {args['steam64id']} inserted_id = {_op.inserted_id}.",
                }
            else:
                return {
                    "success": False,
                    "msg": f"{self.error_preamble}{args['steam64id']} already registered.",
                }
