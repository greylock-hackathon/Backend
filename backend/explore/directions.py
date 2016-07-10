import googlemaps
from datetime import datetime
import json
import re

API_KEY = 'AIzaSyDtu5AMA_k_Md2c-oFYM0VXmPQ1gOvuvec'

def get_directions(start, end):
    gmaps = googlemaps.Client(key=API_KEY)

    now = datetime.now()

    directions = gmaps.directions(
        start,
        end,
        mode='driving',
        departure_time=now
    )

    return directions

def format_directions_json(directions):
    regex = re.compile(r'<.*?>')
    formatted_directions = []
    for step in directions[0]['legs'][0]['steps']:
        full_step = step['html_instructions'] + ' in ' + step["distance"]["text"]
        formatted_directions.append(regex.sub('',full_step))
    return formatted_directions

if __name__ == '__main__':
    directions = get_directions(
        '655 Gilbert Ave Menlo Park California',
        'Palo Alto Caltrain Station'
    )
    formatted_directions = format_directions_json(directions)
    for direction in formatted_directions:
        print direction
