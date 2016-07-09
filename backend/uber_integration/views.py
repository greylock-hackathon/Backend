from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render
from rauth import OAuth2Service
import sys
import requests

def index(request):
    return HttpResponse("Hello, world. You're at the uber integration index.")

#sandbox where we test different uber related services
def sandbox(request):
    return render(request, 'uber_integration/sandbox.html', {})

def get_key(key_num):
    file = open('../../keys.txt', 'r')
    uber_key = file.read()
    print >> sys.stderr, uber_key
    return uber_key

def authenticate(request):
    uber_api = OAuth2Service(
    client_id='vvXhhV_qjiVbwcADOtvVjCK2aj91RJJd',
    client_secret= 'NX_tpqkReG6xzzA2JA26867pq5XLc7y4GWGSkFwn', #get_key(0), #'INSERT_CLIENT_SECRET',
    name='Greylock Hackfest',
    authorize_url='https://login.uber.com/oauth/authorize',
    access_token_url='https://login.uber.com/oauth/token',
    base_url='https://api.uber.com/v1/',
)

    parameters = {'response_type': 'code','scope': 'profile'}

	#### Redirect user here to authorize your application
    login_url = uber_api.get_authorize_url(**parameters)
    return HttpResponse("Succesful Authentication" + login_url)

def authentication_callback(request):
    if request.GET.get('code'):
        message = 'You submitted: %r' % request.GET['code']
        print >> sys.stderr, message
    return HttpResponse("Callback Handled" + message)
