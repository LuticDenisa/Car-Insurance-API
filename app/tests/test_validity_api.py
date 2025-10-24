from datetime import date, timedelta
from app.db.session import get_session
from app.db.repositories import get_active_policy_on_date

def test_validity_true(client, seed_owner_car):
    car = seed_owner_car("VIN-VAL-TRUE")

    # 1 creare polita care acopera azi
    payload = {
    "start_date": date.today().isoformat(),
    "end_date": (date.today() + timedelta(days=1)).isoformat(),
    "provider": "TestCo"
}

    r_post = client.post(f"/api/cars/{car.id}/policies", json=payload)
    assert r_post.status_code == 201, r_post.get_data(as_text=True)
    print("POST /policies response:", r_post.get_json())

    # 2 verifica daca polita exista in db pe azi
    with client.application.app_context():
        s = get_session()
        p = get_active_policy_on_date(s, car.id, date.today())
        print("DEBUG active policy today exists?:", bool(p))
        if p:
            print("DEBUG policy dates:", p.start_date, p.end_date, "provider:", p.provider)

    # 3 endpoint de validitare 
    r_get = client.get(f"/api/cars/{car.id}/insurance-valid?date={date.today().isoformat()}")
    print("GET /insurance-valid:", r_get.status_code, r_get.get_json())
    assert r_get.status_code == 200
    assert r_get.get_json()["valid"] is True

def test_validity_404(client):
    r = client.get("/api/cars/999999/insurance-valid?date=2025-01-01")
    assert r.status_code == 404

def test_validity_400_date_range(client, seed_owner_car):
    car = seed_owner_car("VIN-VAL-400")
    r = client.get(f"/api/cars/{car.id}/insurance-valid?date=1800-01-01")
    assert r.status_code == 400
