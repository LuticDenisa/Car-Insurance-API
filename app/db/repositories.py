from typing import Iterable, Optional
from sqlalchemy import select, and_
from sqlalchemy.orm import Session
from datetime import date

from app.db.models import Owner, Car, InsurancePolicy, Claim

# ========== Owners ==========
def get_owner_by_id(session: Session, owner_id: int) -> Optional[Owner]:
    return session.get(Owner, owner_id)

def get_all_owners(session: Session) -> list[Owner]:
    return session.scalars(select(Owner)).all()


# ========== Cars ==========
def get_car_by_id(session: Session, car_id: int) -> Optional[Car]:
    return session.get(Car, car_id)

def get_cars_with_owner(session: Session) -> list[Car]:
    return session.scalars(select(Car)).all()


# ========== Insurance Policies ==========
def create_policy(session: Session, policy: InsurancePolicy) -> InsurancePolicy:
    session.add(policy)
    session.commit()
    session.refresh(policy)
    return policy

def get_policies_for_car(session: Session, car_id: int) -> list[InsurancePolicy]:
    statement = select(InsurancePolicy).where(InsurancePolicy.car_id == car_id)
    return session.scalars(statement).all()

def get_active_policy_on_date(session: Session, car_id: int, d: date) -> Optional[InsurancePolicy]:
    statement = (
        select(InsurancePolicy)
        .where(
            and_(
                InsurancePolicy.car_id == car_id,
                InsurancePolicy.start_date <= d,
                InsurancePolicy.end_date >= d,
            )
        )
        .limit(1)
    )
    return session.scalars(statement).first()


# ========== Claims ==========
def create_claim(session: Session, claim: Claim) -> Claim:
    session.add(claim)
    session.commit()
    session.refresh(claim)
    return claim

def get_claims_for_car(session: Session, car_id: int) -> list[Claim]:
    statement = select(Claim).where(Claim.car_id == car_id)
    return session.scalars(statement).all()