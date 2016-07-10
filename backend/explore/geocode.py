import googlemaps
import json

API_KEY = 'AIzaSyDtu5AMA_k_Md2c-oFYM0VXmPQ1gOvuvec'

gmaps = googlemaps.Client(key=API_KEY)

def geocode(address):
    result = gmaps.geocode(address)[0]
    return {
        'lat': result['geometry']['location']['lat'],
        'lng': result['geometry']['location']['lng']
    }

def reverse_geocode(lng, lat):
    return gmaps.reverse_geocode((lat, lng))[0]['formatted_address']

if __name__ == '__main__':
    ll = geocode('1010 Bush st., San Francisco')
    print(ll)
    print(reverse_geocode(-73.961452,40.714224))
