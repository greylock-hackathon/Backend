import sys, os
explore_dir = os.path.dirname(os.path.realpath(__file__)) + '/../explore'
sys.path.append(explore_dir)

import json
from django.shortcuts import render
from django.http import HttpResponse
from uber_rides.auth import AuthorizationCodeGrant
from uber_rides.client import UberRidesClient
from django.views.decorators.csrf import csrf_exempt
from subprocess import call
from twilio import twiml
from constants import *
from django.shortcuts import render
from geocode import geocode
from directions import *
from places import *

credential = None
client = None
auth_flow = None
text = ''

# authenticate()

def authenticate():
    global auth_flow
    auth_flow = AuthorizationCodeGrant(
        'vvXhhV_qjiVbwcADOtvVjCK2aj91RJJd',
        {'request'},
        'LDqbDapADdf_ZFeZRe9fL_MKLga3mZ9Ryo3eIHMC',
        'http://localhost:8000/uber/redirect'
    )
    auth_url = auth_flow.get_authorization_url()
    call(['open', auth_url])

def request_ride(start, end):

    response = client.get_products(start[0], start[1])
    products = response.json.get('products')
    product_id = products[0].get('product_id')

    response = client.request_ride(
        product_id=product_id,
        start_latitude=start[1],
        start_longitude=-start[0],
        end_latitude=end[1],
        end_longitude=end[0],
    )
    ride_details = response.json
    ride_id = ride_details.get('request_id')

def index(request):
    return render(request, 'index.html', {}) 

@csrf_exempt
def redirect(request):
    state = request.GET.get('state')
    code = request.GET.get('code')
    url = 'http://localhost:8000/uber_integration/redirect/?state={state}&code={code}'.format(state=state, code=code)
    print(url)
    try:
        session = auth_flow.get_session(url)
    except Exception as e:
        print 'ERROR: ', e
        return HttpResponse('Error: ' + str(e))

    client = UberRidesClient(session, sandbox_mode=True)

    return HttpResponse('authentication successful')

@csrf_exempt
def new_message(request):
    r = twiml.Response()
    data = json.loads(str(request.POST['Body']))

    if data[0] == UBER:
        typ, lng, lat, dest = data
        dest_coords = geocode(dest)
        r.sms(json.dumps(dest_coords))
        print(dest_coords)
    elif data[0] == EXPLORE:
        r.sms('explore')
        typ, query, lng, lat = data
        print(typ, query, lng, lat)
    elif data[0] == DIRECTIONS:
        r.sms('directions')
        typ, choice = data
        print(typ, choice)
    elif data[0] == HELP:
        places = get_places('-122.1430','37.4419')
        encoded_message = encode_places(places)
        print json.dumps(encoded_message) 
        r.sms(json.dumps(encoded_message))
    else:
        r.sms('not supported')

    return HttpResponse(str(r))

def texts(request):
    return HttpResponse(text)
