from googleplaces import GooglePlaces, types

API_KEY = 'AIzaSyDtu5AMA_k_Md2c-oFYM0VXmPQ1gOvuvec'

def get_places(lng, lat, query):
    google_places = GooglePlaces(API_KEY)


    query_result = google_places.nearby_search(
        lat_lng={
            'lat': lat,
            'lng': lng
        },
        keyword=query,
        radius=10000,
        # types=types_
    )

    return [{
        'name': place.name,
        'lng': float(place.geo_location['lng']),
        'lat': float(place.geo_location['lat']),
        'id': place.place_id
    } for place in query_result.places]

def encode_places(places):
    return [[
        1,
        place['lng'],
        place['lat'],
        place['name']
    ] for place in places[:4]]

if __name__ == '__main__':
    places = get_places(-122.1430, 37.4419, 'hospital')
    print(places)
    print '======='
    print encode_places(places)
