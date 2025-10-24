from __future__ import annotations

from datetime import date, datetime, time, timezone
from typing import Optional

import structlog
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import and_, select

from app.db.session import get_session, close_session
from app.db.models import InsurancePolicy

log = structlog.get_logger(__name__)
_scheduler: Optional[BackgroundScheduler] = None


def _now_local() -> datetime:
    # ora locala a serverului
    return datetime.now()


def _today_window_local() -> tuple[datetime, datetime]:
    # Compute window [today 00:00, today 01:00) in server local time
    today = date.today()
    start = datetime.combine(today, time(0, 0, 0))
    end = datetime.combine(today, time(1, 0, 0))
    return start, end


def _detect_and_log_expired_policies(app) -> None:
    """
    Find policies with end_date == today and not yet logged.
    Emit one log per policy
    """

    with app.app_context():
        session = get_session()
        try:
            today = date.today()

            statement = select(InsurancePolicy).where(
                and_(
                    InsurancePolicy.end_date == today,
                    InsurancePolicy.logged_expiry_at.is_(None),
                )
            )
            policies = session.scalars(statement).all()

            if not policies:
                return

            for p in policies:
                msg = f"Policy {p.id} for car {p.car_id} expired on {p.end_date.isoformat()}"
                log.info(
                    "policy_expired",
                    policy_id=p.id,
                    car_id=p.car_id,
                    end_date=p.end_date.isoformat(),
                    message=msg,
                )
                # marcare ca procesată
                p.logged_expiry_at = datetime.now(timezone.utc)

            session.commit()

        except Exception as e:
            session.rollback()
            log.exception("expiry_job_failed", error=str(e))
        finally:
            close_session(None)


def start_scheduler(app) -> BackgroundScheduler:
    """
    Start ApScheduler in background, cu job la fiecare 10 mins.
    Idempotent - nu porneste de doua ori
    """
    global _scheduler
    if _scheduler:
        return _scheduler

    _scheduler = BackgroundScheduler()
    _scheduler.add_job(
        _detect_and_log_expired_policies,
        trigger="interval",
        minutes=10,
        args=[app],
        id="policy_expiry_job",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
        misfire_grace_time=60,
    )
    _scheduler.start()
    log.info("scheduler_started", job_id="policy_expiry_job", interval_min=10)
    return _scheduler


def shutdown_scheduler() -> None:
    global _scheduler
    if _scheduler:
        try:
            _scheduler.shutdown(wait=False)
            log.info("scheduler_stopped")
        finally:
            _scheduler = None

# util pt teste manuale 
def run_expiry_job_once(app) -> None:
    _detect_and_log_expired_policies(app)
