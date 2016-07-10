from django.shortcuts import render
from django.http import HttpResponse
from uber_rides.auth import AuthorizationCodeGrant
from uber_rides.client import UberRidesClient
from django.views.decorators.csrf import csrf_exempt
from subprocess import call

credential = None
client = None

auth_flow = AuthorizationCodeGrant(
    'vvXhhV_qjiVbwcADOtvVjCK2aj91RJJd',
    {'request'},
    'LDqbDapADdf_ZFeZRe9fL_MKLga3mZ9Ryo3eIHMC',
    'http://localhost:8000/uber_integration/redirect'
)
auth_url = auth_flow.get_authorization_url()
call(['open', auth_url])

def index(request):
    return HttpResponse('ok')

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
        return HttpResponse('redirect failed')

    client = UberRidesClient(session, sandbox_mode=True)
    credentials = session.oauth2credential

    response = client.get_products(37.77, -122.41)
    products = response.json.get('products')
    product_id = products[0].get('product_id')

    response = client.request_ride(
        product_id=product_id,
        start_latitude=37.77,
        start_longitude=-122.41,
        end_latitude=37.79,
        end_longitude=-122.41,
    )
    ride_details = response.json
    ride_id = ride_details.get('request_id')

    return HttpResponse(ride_id)
