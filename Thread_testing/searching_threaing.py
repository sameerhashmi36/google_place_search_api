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
# st = time.time()
# t1 = Thread(target=search_places, args = ('school', 200, 23.79172, 90.38023))
# t2 = Thread(target=search_places, args = ('hospital', 200, 23.79172, 90.38023))
# t1.start()
# t2.start()
# t1.join()
# t2.join()
# et = time.time()

# print("threaded Time taken: ",et-st)

def locations_school():

    global data
    
    for i in range(0, 3400, 100):
        print("school: ",i)
        data = search_places('school', i, 23.79172, 90.38023)

def locations_mosque():

    global data

    for i in range(0, 3400, 100):
        print("mosque: ",i)
        data = search_places('mosque', i, 23.79172, 90.38023)

data = None

st = time.time()

t1 = Thread(target=locations_school)
t2 = Thread(target=locations_mosque)

t1.start()
t2.start()

t1.join()
t2.join()

et = time.time()

print(data)

print("threaded Time taken: ",et-st)

