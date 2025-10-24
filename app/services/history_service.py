from sqlalchemy.orm import Session

from app.db.repositories import get_car_by_id, get_policies_for_car, get_claims_for_car

class NotFoundError(Exception): ...


def get_car_history(session: Session, car_id: int) -> list[dict]:
    car = get_car_by_id(session, car_id)
    if not car:
        raise NotFoundError(f"Car with id {car_id} not found.")
    
    policies = get_policies_for_car(session, car_id)
    claims = get_claims_for_car(session, car_id)

    events: list[dict] = []

    for p in policies:
        events.append({
            "type": "POLICY",
            "policyId": p.id,
            "startDate": p.start_date.isoformat(),
            "endDate": p.end_date.isoformat(),
            "provider": p.provider,
        })

    for c in claims:
        events.append({
            "type": "CLAIM",
            "claimId": c.id,
            "claimDate": c.claim_date.isoformat(),
            "amount": float(c.amount),
            "description": c.description,
        })

    
    def event_sort_key(event: dict):
        return event.get("startDate") or event.get("claimDate")


    events.sort(key=event_sort_key)

    return events