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
import requests
import sched, time
from threading import Thread
from twilio.rest import TwilioRestClient

TWILIO_ACCOUNT = 'AC2ed8476d12f01faf112a0f15317233e0'
TWILIO_TOKEN = '1bbb8deb9dc872fbb3cb864dcd7b4eed'
twilio_client = TwilioRestClient(TWILIO_ACCOUNT, TWILIO_TOKEN)

credential = None
client = None
auth_flow = None
text = ''
ride_requests = []

def start_uber_poll():
    s = sched.scheduler(time.time, time.sleep)
    s.enter(5, 1, poll_uber_message, (s,))
    s.run()

def poll_uber_message(sc):
    global ride_status
    r = requests.get('http://130.211.120.248:8000/uber/poll/')
    print(r.json())
    res = r.json()
    if len(res):
        ride = res[0]
        ride_status = request_ride(ride['start'], ride['end'])
        update = requests.post('http://130.211.120.248:8000/uber/update/', ride_status)
    sc.enter(5, 1, poll_uber_message, (sc,))

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

if os.environ.get('LOCAL') == 'true':
    authenticate()

def request_ride(start, end):
    response = client.get_products(start['lat'], start['lng'])
    products = response.json.get('products')
    product_id = products[1].get('product_id')

    return {
        'driver': 'lil b',
        'license_plate': 'a35il44',
        'eta': 10000000,
        'car': 'Toyota'
    }
    '''
    response = client.request_ride(
        product_id=product_id,
        start_latitude=start['lat'],
        start_longitude=start['lng'],
        end_latitude=end['lat'],
        end_longitude=end['lng'],
    )
    ride_details = response.json
    ride_id = ride_details.get('request_id')
    '''

def index(request):
    return render(request, 'index.html', {})

@csrf_exempt
def redirect(request):
    global client
    state = request.GET.get('state')
    code = request.GET.get('code')

    url = 'http://localhost:8000/uber/redirect/?state={state}&code={code}'.format(state=state, code=code)

    try:
        session = auth_flow.get_session(url)
    except Exception as e:
        print 'ERROR: ', e
        return HttpResponse('Error: ' + str(e))

    client = UberRidesClient(session, sandbox_mode=True)

    if os.environ.get('LOCAL') == 'true':
        thread = Thread(target=start_uber_poll)
        thread.start()

    return HttpResponse('authentication successful')

@csrf_exempt
def new_message(request):
    r = twiml.Response()
    data = json.loads(str(request.POST['Body']))

    if data[0] == UBER:
        typ, lng, lat, dest = data
        dest_coords = geocode(dest)
        r.sms(json.dumps(dest_coords))
        ride_requests.append({'start': {'lng': lng, 'lat': lat}, 'end': dest_coords})
    elif data[0] == EXPLORE:
        r.sms('explore')
        typ, query, lng, lat = data
        print(typ, query, lng, lat)
    elif data[0] == DIRECTIONS:
        r.sms('directions')
        typ, choice = data
        print(typ, choice)
    elif data[0] == HELP:
        r.sms('help')
    else:
        r.sms('not supported')

    return HttpResponse(str(r))

def uber_poll(request):
    global ride_requests
    current = None
    try:
        current = json.dumps(ride_requests)
        ride_requests = []
    except Exception as e:
        return HttpResponse(json.dumps({'error': str(e)}), content_type='application/json')
    return HttpResponse(current, content_type='application/json')

@csrf_exempt
def uber_update(request):
    print(request.POST)
    twilio_client.messages.create(to='+15714712696', from_='+12407021303', body=json.dumps(['data']))
    return HttpResponse('ok')
