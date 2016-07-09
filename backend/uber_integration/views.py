from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse("Hello, world. You're at the uber integration index.")

#sandbox where we test different uber related services
def sandbox(request):
    return render(request, 'uber_integration/sandbox.html', {})
