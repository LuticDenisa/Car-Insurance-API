from datetime import date
from sqlalchemy.orm import Session

from app.db.repositories import get_car_by_id, get_active_policy_on_date

class NotFoundError(Exception):
    pass

def is_car_insured_on_date(session: Session, car_id: int, d: date) -> bool:
    car = get_car_by_id(session, car_id)
    if not car:
        raise NotFoundError(f"Car with id {car_id} not found.")
    
    policy = get_active_policy_on_date(session, car_id, d)
    return policy is not None