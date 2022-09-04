from urllib.parse import urlencode
import requests
from threading import Thread
from time import sleep
import time


places_api_key = ""
geocoding_api = ""

def search_places(place_type, searching_radius, lat, lng):
    base_endpoint_places = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    params = {
        "key": places_api_key,
        "input": place_type,
        "inputtype": "textquery",
        "fields": "place_id,formatted_address,name,geometry,permanently_closed"
    }
    locationbias = f"point:{lat},{lng}"
    use_cirular = True
    if use_cirular:
        radius = searching_radius
        locationbias = f"circle:{radius}@{lat},{lng}"

    params['locationbias'] = locationbias

    params_encoded = urlencode(params)
    places_endpoint = f"{base_endpoint_places}?{params_encoded}"

    r = requests.get(places_endpoint)
    return r.json()

place_type = ['school', 'mosque']
searching_radius = 3400
st = time.time()

for i in range(0,searching_radius,100):
    print(i)
    for type_ in place_type:
        place_name = search_places(type_, i, 23.79172, 90.38023)
        try:
            global place
            place = place_name['candidates'][0]['name']
        except:
            # print(i)
            pass


et = time.time()

print(place)
print("Normal Time taken: ",et-st)

