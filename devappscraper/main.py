import geocoder
from .scraper import get_applications



def get_applist(url, delay):
    """Scrapes a given search url and returns a GeoJSON object. Pasuses delay amout of time between requesting pages."""
    result={"type":"FeatureCollection","features":[]}
    applist = get_applications('https://app01.ottawa.ca/postingplans/appDetails.jsf?lang=en&appId=__',url,delay)
    for app in applist:
        coordinates = []
        if len(app['Address'])>0:
            coordinates = get_latlong(app['Address'][0])
            if(coordinates):
                coordinates.reverse()
                result["features"].append({"type": "Feature","geometry":{"type":"Point","coordinates":coordinates },"properties":app})

    return result


def get_latlong(address):
    '''gets the latitude and logngetude from address'''
    return geocoder.ottawa(address).latlng
