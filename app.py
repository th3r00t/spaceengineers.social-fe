import json

from flask import Flask, render_template, request
from markupsafe import escape
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
api_keys = ["000111000111"]
# https://werkzeug.palletsprojects.com/en/2.2.x/middleware/proxy_fix/#werkzeug.middleware.proxy_fix.ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app)
# app.logger.debug('A value for debugging')
# app.logger.warning('A warning occurred (%d apples)', 42)
# app.logger.error('An error occurred')


def get_data(req):
    return json.loads(req)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/path/<path:subpath>")
def show_subpath(subpath):
    return f"Subpath {escape(subpath)}"


# @app.route('/api/post/<path:route>', methods=['GET', 'POST'])
@app.route("/api/post/", methods=["GET", "POST"])
def api_entrypoint():
    if request.method == "POST":
        try:
            _data = get_data(request.data)
            api_key = _data["api_key"]
            breakpoint()
            if api_key in api_keys:
                try:
                    # Has an endpoint been requested?
                    _data["endpoint"]
                except KeyError:
                    # If no endpoint has been requested return api key verification
                    return f"key: {escape(api_key)} Verified"
        except KeyError:
            return "<p><h2>Error No Key Provided With Your Request</h2></p>"
