from googleplaces import GooglePlaces, types

API_KEY = 'AIzaSyDtu5AMA_k_Md2c-oFYM0VXmPQ1gOvuvec'

def get_places(lng, lat):
    google_places = GooglePlaces(API_KEY)

    query_result = google_places.nearby_search(
        lat_lng={
            'lat': lat,
            'lng': lng
        },
        keyword='',
        radius=10000,
        types=[types.TYPE_HOSPITAL]
    )

    if query_result.has_attributions:
        print query_result.html_attributions

    return [{
        'name': place.name,
        'lng': float(place.geo_location['lng']),
        'lat': float(place.geo_location['lat']),
        'id': place.place_id
    } for place in query_result.places]

def encode_places(places):
    encoded_places = []
    for place in places[:4]:
        encoded_places.append(str(place['lat'])[:7])
        encoded_places.append(str(place['lng'])[:7])
        encoded_places.append(place['name'][:30])
    return encoded_places

if __name__ == '__main__':
    places = get_places(-122.1430, 37.4419)
    print(places)
    print '======='
    print encode_places(places)
