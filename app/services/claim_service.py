from datetime import date, datetime, timezone
from decimal import Decimal
from sqlalchemy.orm import Session

from app.db.models import Claim
from app.db.repositories import get_car_by_id, create_claim

class NotFoundError(Exception): ...
class ValidationError(Exception): ...


def register_claim(
        session: Session,
        car_id: int,
        claim_date: date,
        description: str,
        amount: Decimal
) -> Claim:
    if not description or not description.strip():
        raise ValidationError("Description must not be empty.")
    if amount is None or amount <= 0:
        raise ValidationError("Amount must be a positive value.")
    
    car = get_car_by_id(session, car_id)
    if not car:
        raise NotFoundError(f"Car with id {car_id} not found.")
    
    claim = Claim(
        car_id=car_id,
        claim_date=claim_date,
        description=description.strip(),
        amount=amount,
        created_at =datetime.now(timezone.utc)
    )

    return create_claim(session, claim)