import json
import urllib.request

fretb = "17.444123,78.305108"
indus_crest = "17.446771,78.281423"
aparna_sarovar = "17.462537,78.310060"


def get_time(origin, destination):
    url = "http://maps.googleapis.com/maps/api/distancematrix/json?"
    url += "origins={0}&destinations={1}&mode=driving&sensor=false"
    url = url.format(str(origin), str(destination))
    response = json.load(urllib.request.urlopen(url))
    driving_time = response['rows'][0]['elements'][0]['duration']['value']
    return driving_time
