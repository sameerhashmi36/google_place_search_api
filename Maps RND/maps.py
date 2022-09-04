from concurrent.futures import thread
from crypt import methods
from flask import Flask, request, jsonify
from math import radians, sin, cos, asin, sqrt
import requests
from urllib.parse import urlencode
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import json

import threading
import time

app = Flask(__name__)

##################### Measuring Distance ##########################

@app.route('/distance', methods=['GET', 'POST'])
def distance():
    if request.method == 'POST':
        lat1 = request.form['latitude_1']
        lon1 = request.form['longitude_1']
        lat2 = request.form['latitude_2']
        lon2 = request.form['longitude_2']

        # The math module contains a function named
        # radians which converts from degrees to radians.
        lon1 = radians(float(lon1))
        lon2 = radians(float(lon2))
        lat1 = radians(float(lat1))
        lat2 = radians(float(lat2))

        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2

        c = 2 * asin(sqrt(a))

        # Radius of earth in kilometers. Use 3956 for miles
        r = 6371

        # calculate the result
        msg = str(c * r)+" km"

        return msg

##################### box ##########################

@app.route('/box', methods = ['GET', 'POST'])
def rectangle_four_coordinates():
    if request.method == 'POST':

        midpoint_lat = request.form['lat']
        midpoint_lng = request.form['lng']

        # return midpoint_lat

        midpoint_lat = float(midpoint_lat)
        midpoint_lng = float(midpoint_lng)

        rightupperpoint_lat, rightupperpoint_lng = midpoint_lat+0.02500, midpoint_lng+0.01583
        upperleftpoint_lat, upperleftpoint_lng = midpoint_lat+0.02500, midpoint_lng-0.01583
        leftdownpoint_lat, leftdownpoint_lng = midpoint_lat-0.01357, midpoint_lng-0.01583
        downrightpoint_lat, downrightpoint_lng = midpoint_lat-0.01357, midpoint_lng+0.01583

        rightuppercoordinates = rightupperpoint_lat,rightupperpoint_lng
        upperleftcoordinates = upperleftpoint_lat,upperleftpoint_lng
        leftdowncoordinates = leftdownpoint_lat,leftdownpoint_lng
        downrightcoordinates = downrightpoint_lat,downrightpoint_lng

        coordinates = {"rightuppercoordinates":rightuppercoordinates, "upperleftcoordinates":upperleftcoordinates, "leftdowncoordinates":leftdowncoordinates, "downrightcoordinates":downrightcoordinates}



        return coordinates

##################### places api locations ##########################

places_api_key = "your google places api key"
geocoding_api = "your google geocoding api key"

def extract_lat_lng(address_or_postalcode, data_type = 'json'):
    endpoint = f"https://maps.googleapis.com/maps/api/geocode/{data_type}"
    params = {"address": address_or_postalcode, "key": geocoding_api}
    url_params = urlencode(params)
    url = f"{endpoint}?{url_params}"
    r = requests.get(url)
    if r.status_code not in range(200, 299): 
        return {}
    latlng = {}
    try:
        latlng = r.json()['results'][0]['geometry']['location']
    except:
        pass
    return latlng.get("lat"), latlng.get("lng")

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
    # print(places_endpoint)

    r = requests.get(places_endpoint)
    # print(r.status_code)
    return r.json()


@app.route('/placeslocations', methods = ['GET','POST'])
def places():
    if request.method == 'POST':

        ################# Requesting form data ###################
        midpoint_lat = request.form['lat']
        midpoint_lng = request.form['lng']
        rightupperpoint_lat = request.form['rightupperpoint_lat']
        rightupperpoint_lng = request.form['rightupperpoint_lng']
        upperleftpoint_lat = request.form['upperleftpoint_lat']
        upperleftpoint_lng = request.form['upperleftpoint_lng']
        leftdownpoint_lat = request.form['leftdownpoint_lat']
        leftdownpoint_lng = request.form['leftdownpoint_lng']
        downrightpoint_lat = request.form['downrightpoint_lat']
        downrightpoint_lng = request.form['downrightpoint_lng']


        ################ converting string to float ################
        midpoint_lat = float(midpoint_lat)
        midpoint_lng = float(midpoint_lng)
        rightupperpoint_lat = float(rightupperpoint_lat)
        rightupperpoint_lng = float(rightupperpoint_lng)
        upperleftpoint_lat = float(upperleftpoint_lat)
        upperleftpoint_lng = float(upperleftpoint_lng)
        leftdownpoint_lat = float(leftdownpoint_lat)
        leftdownpoint_lng = float(leftdownpoint_lng)
        downrightpoint_lat = float(downrightpoint_lat)
        downrightpoint_lng = float(downrightpoint_lng)


        lat1, lng1 = midpoint_lat, midpoint_lng
        place_type = ['mosque', 'school', 'road', 'river']
        searching_radius = 3400 #meters

        places_ = set()
        # locations = []
        # start_time = []
        # end_time = []

        for i in range(0,searching_radius,100):
            for type in place_type:
                start_time = time.time()
                place_name = search_places(type, i, lat1, lng1)
                # print("!!!!!!!!!!!!", place_name)
                # place_name = threading.Thread(target=search_places, args=(type, i, lat1, lng1))
                # print("!!!!!!!!!!!!", place_name)
                # place_name.start()
                end_time = time.time()
                # print("Place Name: ", place_name)
                try:
                    place = place_name['candidates'][0]['name']
                except:
                    print(i)
                    # pass
                places_.add(place+", Bangladesh")

            print("end_time-start_time: ",end_time-start_time)
        # print("end_time-start_time: ",end_time-start_time)
        
        locations = []
        for i, s in enumerate(places_):
            # print(f"index: {i}, places: {s}")
            
            lat_lng = extract_lat_lng(s)
            locations.append(lat_lng)
            # print(locations)

        polygon = Polygon([
            (rightupperpoint_lat, rightupperpoint_lng),
            (upperleftpoint_lat, upperleftpoint_lng),
            (leftdownpoint_lat, leftdownpoint_lng),
            (downrightpoint_lat, downrightpoint_lng),
            (rightupperpoint_lat, rightupperpoint_lng)
        ])

        total = 0
        count = 0

        inside_rec = []

        for i, s in enumerate(locations):
            # print("i: ",i[0])
            total += 1
            # print("############", i)
            point = Point(s)

            if polygon.contains(point):
                count += 1

                inside_rec.append({str(i):(point.x,point.y)})
        return json.dumps(inside_rec)
        # return {'Total':total,' Count':count}



if __name__ == '__main__':

	app.run(threaded = True)