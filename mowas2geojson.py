from flask import Blueprint
from flask import jsonify
from flask import request
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
@mowas2geojson.route('/mowas_converter/urls', methods=['GET'])
@mowas2geojson.route('/mowasconverter/urls', methods=['GET'])
def get_mowas_urls():
    urlsbase = request.base_url[:-len("/urls")] if request.base_url.endswith("/urls") else request.base_url
    mowasurls = {}
    for key in urls.keys():
        if urls[key].startswith('http'):
            mowasurls[key] = urls[key]
        else:
            mowasurls[key] = urlsbase + "/geojson" + urls[key]
    return jsonify(mowasurls)


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
            # FIXME check for geomtype ("polygon" in "area" or "circle"...
            if isinstance(mwm["info"][0]["area"], list) and "polygon" in mwm["info"][0]["area"][0]:
                feature["geometry"] = mowasgeom2geojsongeom(mwm["info"][0]["area"][0]["polygon"][0], "polygon")
            elif "circle" in mwm["info"][0]["area"]:
                feature["geometry"] = mowasgeom2geojsongeom(mwm["info"][0]["area"]["circle"], "point")
            for property in mwm:
                feature["properties"][property] = mwm[property]
            geojson["features"].append(feature)
    # do something

    return geojson

def mowasgeom2geojsongeom(mowasgeom, geomtype):
    coordlist = [[]]
    mwgeomlist = mowasgeom.split(" ")
    if geomtype == "polygon":
        for g in mwgeomlist:
            lon, lat = g.split(",")
            coordlist[0].append((float(lon), float(lat)))
        mwpolygon = geojson.Polygon(coordlist)
        if not mwpolygon.is_valid:
            print mwpolygon.errors()
        result = mwpolygon
    # FIXME this is not correct yet
    # haha and they canged lonlat to latlon
    elif geomtype == "point":
        for g in mwgeomlist:
            if "," in g:
                lon, lat = g.split(",")
                coordlist[0].append((float(lat), float(lon)))

        mwpoint = geojson.Point(coordlist[0][0])
        if not mwpoint.is_valid:
            print mwpoint.errors()
        result = mwpoint
    return result
