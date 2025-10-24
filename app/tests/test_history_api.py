from datetime import date

def test_history_events_order(client, seed_owner_car):
    car = seed_owner_car("VIN-HIS-001")

    # 2 polite pe ani diferiti
    client.post(f"/api/cars/{car.id}/policies", json={
        "start_date": "2023-01-01", "end_date": "2023-12-31", "provider": "AXA"
    })
    client.post(f"/api/cars/{car.id}/policies", json={
        "start_date": "2024-01-01", "end_date": "2024-12-31", "provider": "Allianz"
    })
    # 2 claims in ani diferiti
    client.post(f"/api/cars/{car.id}/claims", json={
        "claimDate": "2023-06-15", "description": "Rear bumper", "amount": 350
    })
    client.post(f"/api/cars/{car.id}/claims", json={
        "claimDate": "2024-05-10", "description": "Windshield", "amount": 500
    })

    r = client.get(f"/api/cars/{car.id}/history")
    assert r.status_code == 200
    events = r.get_json()

    got = [(e["type"], e.get("startDate") or e.get("claimDate")) for e in events]
    expected = [
        ("POLICY", "2023-01-01"),
        ("CLAIM",  "2023-06-15"),
        ("POLICY", "2024-01-01"),
        ("CLAIM",  "2024-05-10"),
    ]
    assert got == expected
