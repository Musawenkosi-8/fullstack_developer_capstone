from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .restapis import get_request, post_review
from .models import CarModel

logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    user = authenticate(username=username, password=password)
    data = {"userName": username}

    if user is not None:
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}

    return JsonResponse(data)


def logout_request(request):
    logout(request)
    return JsonResponse({"status": 200})


def get_dealerships(request, state=None):
    endpoint = "fetchDealers"
    if state and state != "All":
        endpoint += "/" + state

    response = get_request(endpoint)
    dealers = response.json()

    return JsonResponse({
        "status": response.status_code,
        "dealers": dealers
    })


def get_dealer_reviews(request, dealer_id):
    response = get_request(f"fetchReviews/dealer/{dealer_id}")
    reviews = response.json()

    return JsonResponse({
        "status": response.status_code,
        "reviews": reviews
    })


def get_dealer_details(request, dealer_id):
    response = get_request(f"fetchDealer/{dealer_id}")
    dealer = response.json()

    return JsonResponse({
        "status": response.status_code,
        "dealer": dealer
    })


@csrf_exempt
def add_review(request):
    data = json.loads(request.body)
    response = post_review(data)

    return JsonResponse({
        "status": response.status_code,
        "review": response.json()
    })


def get_cars(request):
    cars = CarModel.objects.select_related("car_make").all()
    return JsonResponse({
        "CarModels": [
            {
                "CarMake": car.car_make.name,
                "CarModel": car.name,
            }
            for car in cars
        ]
    })
