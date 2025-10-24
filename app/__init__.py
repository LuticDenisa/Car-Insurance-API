from flask import Flask
from sqlalchemy import create_engine

from app.core.config import settings
from app.core.logging import setup_logging

from app.db.session import get_session, close_session
from app.db.base import Base

from app.api.routers.cars import blp as cars_blp
from app.api.routers.policies import blp as policies_blp
from app.api.routers.validity import blp as validity_blp
from app.api.routers.claims import blp as claims_blp
from app.api.routers.history import blp as history_blp
from app.api.errors import blp as errors_blp
from app.api.routers.health import blp as health_blp

from app.core.scheduling import start_scheduler


def create_app() -> Flask:
    setup_logging(settings.LOG_LEVEL)

    app = Flask(__name__)
    app.config["DATABASE_URL"] = settings.DATABASE_URL
    app.config["SCHEDULER_ENABLED"] = settings.SCHEDULER_ENABLED

    app.register_blueprint(cars_blp)
    app.register_blueprint(policies_blp)
    app.register_blueprint(validity_blp)
    app.register_blueprint(claims_blp)
    app.register_blueprint(history_blp)
    app.register_blueprint(errors_blp)
    app.register_blueprint(health_blp)

    @app.route("/")
    def home():
        return "Welcome to the Car Insurance API!"
    
    # @app.route("/health")
    # def health():
    #     return {"status": "ok"}, 200
    
    @app.get("/boom")
    def boom():
        raise RuntimeError("boom for tests")

    if app.config.get("SCHEDULER_ENABLED", False):
        start_scheduler(app)

    return app


app = create_app()

@app.before_request
def _bind_session():
    _ = get_session()

@app.teardown_appcontext
def _shutdown_session(exception=None):
    close_session(exception)

def _ensure_db():
    url = app.config["DATABASE_URL"]
    connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
    engine = create_engine(url, future=True, connect_args=connect_args)
    Base.metadata.create_all(bind=engine)

# _ensure_db()