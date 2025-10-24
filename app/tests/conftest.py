import os
import tempfile
import pytest
from sqlalchemy import create_engine
from app import create_app
from app.db.base import Base
from app.db.session import _dispose_all_engines

_dispose_all_engines()


# creez bd temporara pt teste
@pytest.fixture(scope="session")
def test_db_path():
    fd, path = tempfile.mkstemp(prefix="test_car_ins_", suffix=".db")
    os.close(fd)
    yield path
    try:
        os.remove(path)
    except FileNotFoundError:
        pass


# creez aplicatia Flask pt teste
@pytest.fixture(scope="session")
def app(test_db_path):
    os.environ["DATABASE_URL"] = f"sqlite:///{test_db_path}"
    os.environ["SCHEDULER_ENABLED"] = "false"  # e de evitat APScheduler în teste
    app = create_app()

    # creez schema bd de test
    url = app.config["DATABASE_URL"]
    engine = create_engine(url, future=True, connect_args={"check_same_thread": False})
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return app


# creez clientul de test 
@pytest.fixture
def client(app):
    return app.test_client()

# functie helper care creeaza date de test
from app.db.session import get_session
from app.db.models import Owner, Car

@pytest.fixture
def seed_owner_car(app):
    def _make(vin="VIN-TST-001"):
        with app.app_context():
            s = get_session()
            owner = Owner(name="Test Owner", email="t@example.com")
            s.add(owner); s.commit()
            car = Car(vin=vin, make="VW", model="Golf", year_of_manufacture=2020, owner_id=owner.id)
            s.add(car); s.commit()
            return car
    return _make
