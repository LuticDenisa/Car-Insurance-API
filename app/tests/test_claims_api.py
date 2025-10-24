from datetime import date

def test_create_claim_success(client, seed_owner_car):
    car = seed_owner_car("VIN-CLM-OK")
    r = client.post(f"/api/cars/{car.id}/claims", json={
        "claimDate": date.today().isoformat(),
        "description": "Rear bumper",
        "amount": 450.00
    })
    assert r.status_code == 201
    assert "Location" in r.headers
    body = r.get_json()
    assert body["carId"] == car.id
    assert float(body["amount"]) == 450.00

def test_create_claim_400_amount(client, seed_owner_car):
    car = seed_owner_car("VIN-CLM-BAD")
    r = client.post(f"/api/cars/{car.id}/claims", json={
        "claimDate": date.today().isoformat(),
        "description": "X",
        "amount": 0
    })
    assert r.status_code == 400

def test_create_claim_404_car(client):
    r = client.post("/api/cars/999999/claims", json={
        "claimDate": "2025-05-10",
        "description": "X",
        "amount": 100
    })
    assert r.status_code == 404
