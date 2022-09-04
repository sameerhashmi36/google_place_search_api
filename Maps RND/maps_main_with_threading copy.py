from dataclasses import dataclass
from flask import Flask, request, jsonify
from math import radians, sin, cos, asin, sqrt
import requests
from urllib.parse import urlencode
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import json

from threading import Thread
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

def extract_lat_lng(address_or_postalcode,key, data_type = 'json'):
    global places_,locations
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

        places_[key].update({"lat":latlng.get("lat"),"lng":latlng.get("lng")})
        locations.append(((latlng.get("lat"), latlng.get("lng")),key))
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

    r = requests.get(places_endpoint)
    return r.json()


################ global variable ##################
places_ = {}
locations = []
#################### type: school(0-1800) #######################
def location_school_0(lat, lng):
    global places_
    searching_radius = 1801
    type_ = 'school'
    for i in range(0,searching_radius,100):
        print(i)
        
        place_name = search_places(type_, i, lat, lng)
        try:
            place = place_name['candidates'][0]['name']
            val = places_.get((type,place),-1)
            if val == -1:
                places_[(type_,place)] = {'type': type_, 'locationName': place}
        except:
            pass

#################### type: school(1800-3400) #######################
def location_school_1(lat, lng):
    global places_
    searching_radius = 3401
    type_ = 'school'
    for i in range(1800,searching_radius,100):
        print(i)
        
        place_name = search_places(type_, i, lat, lng)
        try:
            place = place_name['candidates'][0]['name']
            val = places_.get((type,place),-1)
            if val == -1:
                places_[(type_,place)] = {'type': type_, 'locationName': place}
        except:
            pass

#################### type: mosque(0-1800) #######################
def location_mosque_0(lat, lng):
    global places_
    searching_radius = 1801
    type_ = 'mosque'
    for i in range(0,searching_radius,100):
        print(i)
        
        place_name = search_places(type_, i, lat, lng)
        try:
            place = place_name['candidates'][0]['name']
            val = places_.get((type,place),-1)
            if val == -1:
                places_[(type_,place)] = {'type': type_, 'locationName': place}
        except:
            pass

#################### type: mosque(1800-3400) #######################
def location_mosque_1(lat, lng):
    global places_
    searching_radius = 3401
    type_ = 'mosque'
    for i in range(1800,searching_radius,100):
        print(i)
        
        place_name = search_places(type_, i, lat, lng)
        try:
            place = place_name['candidates'][0]['name']
            val = places_.get((type,place),-1)
            if val == -1:
                places_[(type_,place)] = {'type': type_, 'locationName': place}
        except:
            pass

#################### type: hospital(0-1800) #######################
def location_hospital_0(lat, lng):
    global places_
    searching_radius = 1801
    type_ = 'hospital'
    for i in range(0,searching_radius,100):
        print(i)
        
        place_name = search_places(type_, i, lat, lng)
        try:
            place = place_name['candidates'][0]['name']
            val = places_.get((type,place),-1)
            if val == -1:
                places_[(type_,place)] = {'type': type_, 'locationName': place}
        except:
            pass

#################### type: hospital(1800-3400) #######################
def location_hospital_1(lat, lng):
    global places_
    searching_radius = 3401
    type_ = 'hospital'
    for i in range(1800,searching_radius,100):
        print(i)
        
        place_name = search_places(type_, i, lat, lng)
        try:
            place = place_name['candidates'][0]['name']
            val = places_.get((type,place),-1)
            if val == -1:
                places_[(type_,place)] = {'type': type_, 'locationName': place}
        except:
            pass


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


        # lat1, lng1 = midpoint_lat, midpoint_lng
        # place_type = ['mosque','school','hospital'] #, 'school', 'road', 'river'
        # searching_radius = 3400 #meters

        # places_ = {}

        # for i in range(0,searching_radius,100):
        #     print(i)
        #     for type_ in place_type:
        #         place_name = search_places(type_, i, lat1, lng1)
        #         try:
        #             place = place_name['candidates'][0]['name']
        #             val = places_.get((type,place),-1)
        #             if val == -1:
        #                 places_[(type_,place)] = {'type': type_, 'locationName': place}
        #         except:
        #             pass

        start_time = time.time()
        ###################### Threads ###########################
        t1 = Thread(target=location_school_0, args=(midpoint_lat, midpoint_lng))
        t2 = Thread(target=location_school_1, args=(midpoint_lat, midpoint_lng))
        t3 = Thread(target=location_mosque_0, args=(midpoint_lat, midpoint_lng))
        t4 = Thread(target=location_mosque_1, args=(midpoint_lat, midpoint_lng))
        t5 = Thread(target=location_hospital_0, args=(midpoint_lat, midpoint_lng))
        t6 = Thread(target=location_hospital_1, args=(midpoint_lat, midpoint_lng))

        ################## starting threads #######################
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        t6.start()


        ################## threads waiting to be finished #######################
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        t6.join()

        thread_end_time = time.time()

        print("Thread time: ", thread_end_time-start_time)
        
        
        
        for i, s in places_.items():
            # print("----------",s['locationName'])
            
            lat_lng = extract_lat_lng(s['locationName']+", Bangladesh",i)
            places_[i].update({"lat":lat_lng[0],"lng":lat_lng[1]})
            locations.append((lat_lng,i))
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

        for i, (lat_long,key) in enumerate(locations):
        
            # print("i: ",i[0])
            total += 1
            point = Point(lat_long)

            if polygon.contains(point):
                count += 1
                
                # inside_rec.append({str(i):(point.x,point.y)})
            else:
                del places_[key]
                
        end_time = time.time()
        print("Total Time taken: ", end_time - start_time)
        
        return json.dumps(list(places_.values()))

        # return {'Total':total,' Count':count}



if __name__ == '__main__':

	app.run(debug = True)