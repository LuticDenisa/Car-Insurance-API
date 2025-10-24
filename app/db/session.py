from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from flask import current_app, g

_engine_cache = {}

def _engine():
    db_url = current_app.config["DATABASE_URL"]
    if db_url not in _engine_cache:
        connect_args = {"check_same_thread": False} if db_url.startswith("sqlite") else {}
        engine = create_engine(db_url, future=True, connect_args=connect_args)

        if db_url.startswith("sqlite"):
            @event.listens_for(engine, "connect")
            def _set_sqlite_pragma(dbapi_conn, conn_record):
                cursor = dbapi_conn.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()

        _engine_cache[db_url] = engine

    return _engine_cache[db_url]

def get_session():
    if "db_session" not in g:
        SessionLocal = sessionmaker(bind=_engine(), autoflush=False, autocommit=False, future=True, expire_on_commit=False)
        g.db_session = SessionLocal()
    return g.db_session

def close_session(e=None):
    db_session = g.pop("db_session", None)
    if db_session is not None:
        db_session.close()

def _dispose_all_engines():
    for eng in _engine_cache.values():
        eng.dispose()
    _engine_cache.clear()
