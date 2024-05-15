import json
from datetime import datetime

from celery import shared_task
from .models import Route
import requests

from datacollector.models import TrashIsland, Trashcan




@shared_task
def create_route(trashcans=None):
    """
    :param trashcans: list of Trashcan objects
    """

    url = "https://graphhopper.com/api/1/vrp"

    query = {}


    headers = {"Content-Type": "application/json"}

    payload = {
        "vehicles": [
            {
                "vehicle_id": "truck",
                "start_address": {
                    "location_id": "home",
                    "lon": 10.0146,
                    "lat": 57.0237
                },
                "return_to_depot": True,
            },
        ],
        "configuration": {
            "routing": {
                "calc_points": False,
                "snap_preventions": [
                    "motorway",
                    "trunk",
                    "tunnel",
                    "bridge",
                    "ferry"
                ]
            }
        }
    }

    for trashcan in trashcans:
        payload["services"].append({
            "id": f"s-{trashcan.id}",
            "address": {
                "location_id": f"{trashcan.island.longitude}_{trashcan.island.latitude}",
                "lon": trashcan.island.longitude,
                "lat": trashcan.island.latitude
            },
        })

    response = requests.post(url, json=payload, headers=headers, params=query)

    data = response.json()
    print(json.dumps(data, indent=2))

    address_string = ""

    for address in data["solution"]["routes"][0]["activities"]:
        address_string += f"{address['address']['lon']},{address['address']['lat']};"

    print(address_string)

    Route.objects.create(
        user=None,
        route_name="Rute 1",
        adresses=address_string,
        operating_date=datetime.now().date(),
    )




if __name__ == "__main__":
    #create_route(Trashcan.objects.all())
    create_route()
