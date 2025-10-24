from datetime import date
from sqlalchemy.orm import Session

from app.db.models import InsurancePolicy
from app.db.repositories import get_car_by_id, create_policy

class ValidationError(Exception): ...
class NotFoundError(Exception): ...


def create_policy_for_car(
        session: Session,
        car_id: int,
        provider: str | None,
        start_date: date,
        end_date: date
) -> InsurancePolicy:
    if end_date <= start_date:
        raise ValidationError("End date must be after start date")
    
    car = get_car_by_id(session, car_id)
    if not car:
        raise NotFoundError(f"Car with id {car_id} not found.")
    
    policy = InsurancePolicy(
        car_id=car_id,
        provider=provider,
        start_date=start_date,
        end_date=end_date
    )

    return create_policy(session, policy)