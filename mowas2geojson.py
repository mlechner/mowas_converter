from flask import Blueprint
from flask import jsonify
from flask import abort
from flask_cors import cross_origin
from os import path
import json
import geojson
# from urllib.parse import urlparse # Pyton 3
from urlparse import urlparse  # Python 2
import urllib2

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
fc_template = {
    "type": "FeatureCollection",
    "features": []
}

f_template = {
    "type": "Feature",
    "geometry": {
        "type": "Polygon",
        "coordinates": []
    },
    "properties": {}
}


@cross_origin()
@mowas2geojson.route('/mowas_converter/geojson/<string:provider>/<string:url>', methods=['GET'])
@mowas2geojson.route('/mowasconverter/geojson/<string:provider>/<string:url>', methods=['GET'])
def get_mowas2geojson(provider, url):
    if "/".join(("", provider, url)) not in urls.values():
        abort(404)
    host = get_host_from_url(configurl)
    mowasurl = "/".join((host, provider, url))
    mowascontents = urllib2.urlopen(mowasurl).read()
    geojson = mowascontents2geojson(mowascontents)
    return jsonify(geojson)

def get_host_from_url(url):
    parsed_uri = urlparse(url)
    result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    return result


def mowascontents2geojson(mowascontents):
    mowasjson = json.loads(mowascontents)
    if isinstance(mowasjson, list):
        geojson = fc_template
        for mwm in mowasjson:
            feature = f_template
            # only one entry per level?
            feature["geometry"] = mowasgeom2geojsongeom(mwm["info"][0]["area"][0]["polygon"][0])
            for property in mwm:
                feature["properties"][property] = mwm[property]
            geojson["features"].append(feature)
    # do something

    return geojson

def mowasgeom2geojsongeom(mowasgeom):
    coordlist = [[]]
    mwgeomlist = mowasgeom.split(" ")
    for g in mwgeomlist:
        lon,lat = g.split(",")
        coordlist[0].append((float(lon), float(lat)))
    mwpolygon = geojson.Polygon(coordlist)
    if not mwpolygon.is_valid:
        print mwpolygon.errors()
    return mwpolygon
