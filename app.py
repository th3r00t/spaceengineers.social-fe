"""Server for spaceengineers.social."""
import json

from flask import Flask, render_template, request
from markupsafe import escape
from werkzeug.middleware.proxy_fix import ProxyFix

from sesocial.sesapi import SESApi

app = Flask(__name__)
api_keys = ["000111000111"]
# https://werkzeug.palletsprojects.com/en/2.2.x/middleware/proxy_fix/#werkzeug.middleware.proxy_fix.ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app)
# app.logger.debug('A value for debugging')
# app.logger.warning('A warning occurred (%d apples)', 42)
# app.logger.error('An error occurred')


def get_data(req):
    """Get data from json object."""
    return json.loads(req)


@app.route("/")
def index():
    """Render the main web based layout."""
    return render_template("index.html")


@app.route("/path/<path:subpath>")
def show_subpath(subpath):
    """Test object for relaying path:subpath objects."""
    return f"Subpath {escape(subpath)}"


# @app.route('/api/post/<path:route>', methods=['GET', 'POST'])
@app.route("/api/post/", methods=["GET", "POST"])
def api_entrypoint():
    """Actual api entrypoint."""
    if request.method == "POST":
        try:
            _data = get_data(request.data)
            api_key = _data["api_key"]
            if api_key in api_keys:
                try:
                    _ep = _data["endpoint"]
                except KeyError:
                    return f"{SESApi().msg_preamble}api key validated"
                try:
                    _args = _data["args"]
                except KeyError:
                    _args = None
                return SESApi().router(_ep, _args)
        except KeyError:
            return f"{SESApi().error_preamble}no key provided with your request"
