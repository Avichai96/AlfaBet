from fastapi.testclient import TestClient
from fastapi import Response


class Globals:
    event_id: int = 0
    event_remainder_id: int = 0


create_event_data = {
        "title": "New Event For Remainder",
        "description": "Event Description",
        "location": "Event Location",
        "venue": "Event Venue",
        "event_date": "2080-01-01T00:00:00",
        "popularity": 10
    }
sign_up_for_reminder_data ={
  "email": "me.test@gmail.com",
  "event_id": 1
}


def test_sign_up_for_reminder(test_client: TestClient):
    response: Response = test_client.post("/events/", json=create_event_data)
    Globals.event_id =  response.json()["id"]
    sign_up_for_reminder_data["event_id"] = Globals.event_id
    response: Response = test_client.post("/reminders/signup-for-reminder/", json=sign_up_for_reminder_data)
    assert response.status_code == 200
    assert response.json()["email"] == sign_up_for_reminder_data["email"]
    Globals.event_remainder_id = response.json()["id"]


def test_unsubscribe(test_client: TestClient):
    response: Response = test_client.post("/reminders/unsubscribe/", params={"reminder_id": Globals.event_remainder_id})
    assert response.status_code == 200
    reminder_details = response.json()["reminder_details"]
    assert reminder_details["unsubscribed"] is True
    response: Response = test_client.delete(f"/events/{Globals.event_id}")
    assert response.status_code == 200
