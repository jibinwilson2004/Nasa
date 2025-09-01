import json
import turtle
import urllib.request
import time
import webbrowser
import geocoder
import os
from math import radians, cos, sin, asin, sqrt

# ----------------------------
# Haversine distance calculator
# ----------------------------
def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Earth radius (km)
    return c * r

# ----------------------------
# Get astronaut data
# ----------------------------
url = "http://api.open-notify.org/astros.json"
response = urllib.request.urlopen(url)
result = json.loads(response.read())

file = open("iss.txt", "w")
file.write('There are currently ' + str(result["number"]) + " astronauts on the ISS:\n\n")

people = result["people"]
for p in people:
    file.write(p["name"] + " - on board\n")

# Get user location
g = geocoder.ip('me')
my_lat, my_lon = g.latlng
file.write('\nYour current lat/long is: ' + str(g.latlng))
file.close()

# Open file in browser
webbrowser.open("file://" + os.path.realpath("iss.txt"))

# ----------------------------
# Setup Turtle screen
# ----------------------------
screen = turtle.Screen()
screen.setup(1280, 720)
screen.setworldcoordinates(-180, -90, 180, 90)

screen.bgpic("map.gif")          # must have map.gif
screen.register_shape("iss.gif") # must have iss.gif

# ISS marker
iss = turtle.Turtle()
iss.shape("iss.gif")
iss.setheading(45)
iss.penup()

# User location marker
location_marker = turtle.Turtle()
location_marker.shape("circle")
location_marker.color("red")
location_marker.penup()
location_marker.goto(my_lon, my_lat)
location_marker.stamp()  # permanent red dot

# Trail marker for ISS path
trail = turtle.Turtle()
trail.hideturtle()
trail.penup()
trail.color("blue")

# ----------------------------
# Live Tracking Loop
# ----------------------------
while True:
    url = "http://api.open-notify.org/iss-now.json"
    response = urllib.request.urlopen(url)
    result = json.loads(response.read())

    location = result["iss_position"]
    lat = float(location["latitude"])
    lon = float(location["longitude"])

    # Move ISS on map
    iss.goto(lon, lat)

    # Leave a blue dot trail
    trail.goto(lon, lat)
    trail.dot(2)

    # Calculate distance to user
    distance = haversine(my_lat, my_lon, lat, lon)

    # Print live data
    print(f"\nLatitude: {lat}")
    print(f"Longitude: {lon}")
    print(f"Distance from you: {distance:.2f} km")

    time.sleep(5)
