from flask import Blueprint
from flask import jsonify
from flask import abort
from flask import request
from flask_cors import cross_origin
from os import path
import json
from collections import OrderedDict
from urllib.parse import urlparse
# from urlparse import urlparse  # Python 2

mowas2geojson = Blueprint('mowas2geojson', __name__)

here = (path.dirname(__file__) + '/') if path.dirname(__file__) else path.dirname(__file__)

configurl = "https://warnung.bund.de/bbk.config/config_rel.json"
urls = {
    "ialertURLTempesti": "/bbk.dwd/unwetter.json",
    "alertURLFlood": "/bbk.wsv/hochwasser.json",
    "alertURLLhp": "/bbk.lhp/hochwassermeldungen.json",
    "alertURLForestfire": "/bbk.dwd/waldbrand.json",
    "alertURLEarthquake": "/bbk.bgr/erdbeben.json",
    "alertURLAnnouncements": "/bbk.mowas/gefahrendurchsagen.json",
    "alertURLAnnouncements2": "/bbk.mowas/gefahrendurchsagen.json",
    "alertURLAnnouncementsChanges": "/bbk.mowas/changes.json",
    "alertURLBaseAnnouncementsPolygon": "/bbk.mowas/polygon",
    "alertURLBaseAnnouncementsGeocode":	"/bbk.mowas/geocode",
    "certa_server_url": "https://api.certa.io/"
}


@cross_origin()
@mowas2geojson.route('/mowas_converter/geojson/<string:url>', methods=['GET'])
@mowas2geojson.route('/mowasconverter/geojson/<string:url>', methods=['GET'])
def get_mowas2geojson(url):
    if url not in urls.values():
        abort(404)
    result_json = {}
    host = get_host_from_url(configurl)
    

    return result_json

def get_host_from url(url):
    parsed_uri = urlparse(url)
    result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    return result
