from flask import Flask
from flask import jsonify

from mowas2geojson import mowas2geojson

app = Flask(__name__)
app_version = "0.0.1-dev"
app.secret_key = 'cH\xc5\xd9\xd2\xc4,^\x8c\x9f3S\x94Y\xe5\xc7!\x06>A'
app.register_blueprint(mowas2geojson)


@app.route('/')
def hello_world():
    return 'There is nothing to be found here!'

@app.route('/version')
@app.route('/mowas_converter/version')
@app.route('/mowasconverter/version')
def version():
    version = {'version': app_version}
    return jsonify(version)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
