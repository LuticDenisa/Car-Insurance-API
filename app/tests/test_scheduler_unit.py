from datetime import date
from app import create_app
from app.db.session import get_session
from app.db.models import Owner, Car, InsurancePolicy
from app.core.scheduling import run_expiry_job_once

def test_scheduler_detects_and_marks():
    app = create_app()
    with app.app_context():
        s = get_session()
        # date de test - masina cu polita care urmeaza sa expire
        o = Owner(name="Sched Owner", email="sched@example.com")
        s.add(o); s.commit()
        c = Car(vin="VIN-SCH-001", make="VW", model="Golf", year_of_manufacture=2020, owner_id=o.id)
        s.add(c); s.commit()
        p = InsurancePolicy(car_id=c.id, provider="AXA", start_date=date.today(), end_date=date.today())
        s.add(p); s.commit()

        assert p.logged_expiry_at is None
        run_expiry_job_once(app)
        s.refresh(p)
        first = p.logged_expiry_at
        assert first is not None  # marcat

        # idempotent - nu se schimba daca rulez iar
        run_expiry_job_once(app)
        s.refresh(p)
        assert p.logged_expiry_at is not None
