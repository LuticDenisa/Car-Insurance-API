from flask import Blueprint, request, jsonify
from app.db.session import get_session
from app.api.schemas import ClaimIn
from app.services.claim_service import register_claim, ValidationError, NotFoundError

blp = Blueprint("claims", __name__)


@blp.post("/api/cars/<int:car_id>/claims")
def create_claim(car_id: int):
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415

    try:
        payload = ClaimIn.model_validate(request.get_json() or {})
    except Exception as e:
        return jsonify({"error": "Invalid payload", "detail": str(e)}), 400

    session = get_session()
    try:
        c = register_claim(
            session=session,
            car_id=car_id,
            claim_date=payload.claimDate,
            description=payload.description,
            amount=payload.amount,
        )
    except ValidationError as ve:
        return jsonify({"error": str(ve)}), 400
    except NotFoundError:
        return jsonify({"detail": "Car not found"}), 404

    resp = jsonify({
        "id": c.id,
        "carId": c.car_id,
        "claimDate": c.claim_date.isoformat(),
        "description": c.description,
        "amount": float(c.amount),
    })
    resp.status_code = 201
    resp.headers["Location"] = f"/api/cars/{car_id}/claims/{c.id}"
    return resp
