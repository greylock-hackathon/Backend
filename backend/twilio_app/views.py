from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from django.http import HttpResponse

def index(request):
    return HttpResponse('hello')

@csrf_exempt
def new_message(request):
    print request.POST
    return HttpResponse('ok')
