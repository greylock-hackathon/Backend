from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from twilio import twiml

# Create your views here.
from django.http import HttpResponse

def index(request):
    return HttpResponse('hello')

@csrf_exempt
def new_message(request):
    print request.POST
    r = twiml.Response()
    r.say(request.POST['Body'])
    return HttpResponse(str(r))
