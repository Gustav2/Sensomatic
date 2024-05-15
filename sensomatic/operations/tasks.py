import json

from celery import shared_task
from .models import Route
import requests

from datacollector.models import TrashIsland, Trashcan

url = "https://graphhopper.com/api/1/vrp"

query = {}
query = {"key": ""}

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


@shared_task
def create_route(trashcans):
    """
    :param trashcans: list of Trashcan objects
    """

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



if __name__ == "__main__":
    create_route(Trashcan.objects.all())
