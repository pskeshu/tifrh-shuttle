import json
import requests

fretb = "17.444123,78.305108"
indus_crest = "17.446771,78.281423"
aparna_sarovar = "17.462537,78.310060"


def get_time(origin, destination, departuretime="0000"):
    url = "http://maps.googleapis.com/maps/api/distancematrix/json"

    traffic_options = {
        "departureTime": departuretime,
        "trafficModel": "bestguess"
    }

    options = {
        "origins": origin,
        "destinations": destination,
        "mode": "driving",
        "drivingOptions": traffic_options,
        "sensor": "false"
    }

    g_maps_estimate = requests.get(url, params=options).content
    distancematrix = json.loads(g_maps_estimate.decode("utf-8"))
    driving_time = distancematrix['rows'][0][
        'elements'][0]['duration']['value']

    return driving_time
