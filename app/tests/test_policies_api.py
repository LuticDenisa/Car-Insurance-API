# test pt validare creare, inclusiv end_Date > start_date

from datetime import date, timedelta

def test_create_policy_success(client, seed_owner_car):
    car = seed_owner_car("VIN-POL-OK")
    payload = {
        "start_date": (date.today() - timedelta(days=10)).isoformat(),
        "end_date": date.today().isoformat(),
        "provider": "AXA"
    }
    r = client.post(f"/api/cars/{car.id}/policies", json=payload)
    assert r.status_code == 201
    body = r.get_json()
    assert body["carId"] == car.id
    assert body["provider"] == "AXA"

def test_create_policy_bad_dates(client, seed_owner_car):
    car = seed_owner_car("VIN-POL-BAD")
    payload = {
        "start_date": "2025-01-10",
        "end_date":   "2025-01-01",  # < start -> invalid
        "provider": "Allianz"
    }
    r = client.post(f"/api/cars/{car.id}/policies", json=payload)
    assert r.status_code == 400  # ValidationError din service

def test_policy_404_car(client):
    r = client.post("/api/cars/999999/policies", json={
        "start_date": date.today().isoformat(),
        "end_date": (date.today()+timedelta(days=1)).isoformat()
    })
    assert r.status_code == 404

