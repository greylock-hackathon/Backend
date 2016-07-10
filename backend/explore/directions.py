import googlemaps
from datetime import datetime

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

if __name__ == '__main__':
    directions = get_directions(
        '655 Gilbert Ave Menlo Park California',
        'Palo Alto Caltrain Station'
    )
