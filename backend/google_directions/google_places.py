from googleplaces import GooglePlaces, types, lang

YOUR_API_KEY = 'AIzaSyDtu5AMA_k_Md2c-oFYM0VXmPQ1gOvuvec'

google_places = GooglePlaces(YOUR_API_KEY)

lat = "37.4419"
lng = "-122.1430"

query_result = google_places.nearby_search(lat_lng={'lat':lat, 'lng':lng}, keyword='',radius=10000, types=[types.TYPE_HOSPITAL])

if query_result.has_attributions:
    print query_result.html_attributions

for place in query_result.places:
    print place.name
    print place.geo_location
    print place.place_id
