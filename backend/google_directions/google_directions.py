import googlemaps
from datetime import datetime


gmaps = googlemaps.Client(key='AIzaSyDtu5AMA_k_Md2c-oFYM0VXmPQ1gOvuvec')

now = datetime.now()
print now
directions_result = gmaps.directions("655 Gilbert Ave Menlo Park California","Palo Alto Caltrain Station",mode="driving",departure_time=now)
print len(directions_result)
print directions_result
