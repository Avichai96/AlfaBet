# tests/test_event_router.py

from fastapi.testclient import TestClient
from fastapi import Response


class Globals:
    event_id: int = 0
    batch_event_ids: list = []

create_event_data = {
        "title": "New Event",
        "description": "Event Description",
        "location": "Event Location",
        "venue": "Event Venue",
        "event_date": "2023-01-01T00:00:00",
        "popularity": 10
    }
update_event_data = {
        "title": "Updated Event",
        "description": "Event Description",
        "location": "Event Location",
        "venue": "Event Venue",
        "event_date": "2023-01-01T00:00:00",
        "popularity": 20
    }
create_batch_events_data = [
    {
        "title": "New Event2",
        "description": "Event Description2",
        "location": "Event Location2",
        "venue": "Event Venue2",
        "event_date": "2023-01-01T00:00:00",
        "popularity": 20
    },
    {

        "title": "New Event3",
        "description": "Event Description3",
        "location": "Event Location3",
        "venue": "Event Venue3",
        "event_date": "2023-01-01T00:00:00",
        "popularity": 30
    }
]
update_batch_event_data = [
    {
        "title": "Updated Event2",
        "description": "Event Description2",
        "location": "Event Location2",
        "venue": "Event Venue2",
        "event_date": "2023-01-01T00:00:00",
        "popularity": 20
    },
    {
        "title": "Updated Event3",
        "description": "Event Description3",
        "location": "Event Location3",
        "venue": "Event Venue3",
        "event_date": "2023-01-01T00:00:00",
        "popularity": 30
    }
]


def test_create_event(test_client: TestClient):
    response: Response = test_client.post("/events/", json=create_event_data)
    assert response.status_code == 200
    assert response.json()["title"] == "New Event"
    Globals.event_id =  response.json()["id"] 


def test_read_event(test_client: TestClient):
    response: Response = test_client.get(f"/events/{Globals.event_id}")
    assert response.status_code == 200
    assert "title" in response.json()


def test_update_event(test_client: TestClient):
    response: Response = test_client.put(f"/events/{Globals.event_id}", json=update_event_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Event"


def test_create_batch_events(test_client: TestClient):
    response: Response = test_client.post("/events/batch", json=create_batch_events_data)
    assert response.status_code == 200
    res_list = response.json()
    for res in res_list:
        Globals.batch_event_ids.append(res["id"])


def test_update_batch_events(test_client: TestClient):
    for count, e in enumerate(update_batch_event_data, start=0):
        e["id"] = Globals.batch_event_ids[count]
    response: Response = test_client.put(f"/events/batch", json=update_batch_event_data)
    assert response.status_code == 200
    res_list = response.json()
    for res in res_list:
        assert res["title"] in ["Updated Event2", "Updated Event3"]


def test_delete_event(test_client: TestClient):
    response: Response = test_client.delete(f"/events/batch", json=Globals.batch_event_ids)
    assert response.status_code == 200


def test_delete_event(test_client: TestClient):
    response: Response = test_client.delete(f"/events/{Globals.event_id}")
    assert response.status_code == 200
