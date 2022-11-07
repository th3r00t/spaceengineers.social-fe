import json
from flask import Flask, request, render_template
#from flask_api_autodoc.view import render_page
from werkzeug.middleware.proxy_fix import ProxyFix
from markupsafe import escape


app = Flask(__name__)
api_keys = ['000111000111']
# https://werkzeug.palletsprojects.com/en/2.2.x/middleware/proxy_fix/#werkzeug.middleware.proxy_fix.ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app)
# app.logger.debug('A value for debugging')
# app.logger.warning('A warning occurred (%d apples)', 42)
# app.logger.error('An error occurred')

def get_data(req):
    return json.loads(req)


@app.route("/")
def index():
    return render_template('index.html')

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    return f'Subpath {escape(subpath)}'

# @app.route('/api/post/<path:route>', methods=['GET', 'POST'])
@app.route('/api/post/', methods=['GET', 'POST'])
def api_entrypoint():
    error = None
    if request.method == 'POST':
        try:
            _data = get_data(request.data)
            api_key = _data['api_key']
            if api_key in api_keys:
                try:
                   endpoint = _data['endpoint'] 
                except KeyError as e:
                    return e
                return f'API_KEY: {escape(api_key)}'
        except KeyError:
            return '<p><h2>Error No Key Provided With Your Request</h2></p>'

# @app.route('/doc')
# def _():
#     return render_page(path_prefixes=['/api'])
