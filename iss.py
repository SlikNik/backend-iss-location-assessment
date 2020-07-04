#!/usr/bin/env python

__author__ = 'Nikal Morgan'

# import sys
import requests
import time
import turtle

icon = 'iss.gif'
w_map = 'map.gif'
base_url = 'http://api.open-notify.org/'
astro = 'astros.json'
current_iss = 'iss-now.json'
ovrhead_iss = 'iss-pass.json'


# Part A
def get_astro_info_list():
    """Request a list of the astronauts currently in space.
    Returns full names, the spacecraft currently on board,
    and the total number of astronauts in space"""
    r = requests.get(base_url + astro)
    r.raise_for_status()
    return r.json()['people']


# Part B
def get_station_current_info():
    """Request current geographic coordinates (lat/lon)
    of the space station, along with a timestamp."""
    r = requests.get(base_url + current_iss)
    r.raise_for_status()
    timestamp = r.json()['timestamp']
    coordinates = r.json()['iss_position']
    lat = float(coordinates['latitude'])
    lon = float(coordinates['longitude'])
    return time.ctime(timestamp), lat, lon


# Part C
def create_iss_w_map(lat, lon):
    """create a graphics screen with the background as map.gif.
    Register an icon image for the ISS within the turtle screen context,
    and move the ISS to its current lat/lon on the map."""
    screen = turtle.Screen()
    screen.setup(720, 360)
    screen.bgpic(w_map)
    screen.setworldcoordinates(-180, -90, 180, 90)

    screen.register_shape(icon)
    iss = turtle.Turtle()
    iss.shape(icon)
    iss.setheading(90)
    iss.penup()
    iss.goto(lon, lat)
    return screen


# Part D
def get_next_overhead(lat, lon):
    """Get the next time that the ISS will be overhead given
    lat and lon; plot a yellow dot on the map."""
    params = {"lat": lat, "lon": lon}
    r = requests.get(base_url + ovrhead_iss, params=params)
    r.raise_for_status()
    ovrhead_time = r.json()['response'][1]['risetime']
    timestamps = time.ctime(ovrhead_time)
    location = turtle.Turtle()
    location.color("yellow")
    location.penup()
    location.goto(lon, lat)
    location.dot(5)
    location.hideturtle()
    location.write(timestamps, align='center',
                   font=("Comic Sans MS", 12, "normal"))
    return timestamps


def main():
    # Part A get list of astronauts with their crafts
    astro_list = get_astro_info_list()
    print(f'Current  astronauts in space: {len(astro_list)}')
    for astro in astro_list:
        print('* {} in {}'.format(astro['name'], astro['craft']))

    # Part B get current coords of ISS with time stamp
    current_iss_info = get_station_current_info()
    timestamp = current_iss_info[0]
    lat = current_iss_info[1]
    lon = current_iss_info[2]
    print(f'Current ISS coordinates: lat={lat:.02f} lon={lon:.02f}')
    print(f'Current ISS timestamp: {timestamp}')

    # Part C show ISS on world map
    screen = None
    try:
        # Trying to show turtle
        screen = create_iss_w_map(lat, lon)

        # Part next overhead time for Indianpolis, IN
        indy_lat = 39.7684
        indy_lon = -86.1581
        iss_next_ovhead_indy = get_next_overhead(indy_lat, indy_lon)
        print(f'Next time ISS will pass over Indy: {iss_next_ovhead_indy}')
    except RuntimeError as err:
        print(f'ERROR: problem loading: {str(err)}')

    if screen is not None:
        print('Click on the screen to exit')
        screen.exitonclick()


if __name__ == '__main__':
    main()
