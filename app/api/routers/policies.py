from flask import Blueprint, request, jsonify, url_for, Response
from datetime import date
from app.db.session import get_session
from app.api.schemas import PolicyIn
from app.services.policy_service import create_policy_for_car, ValidationError, NotFoundError


blp = Blueprint("policies", __name__)


@blp.post("/api/cars/<int:car_id>/policies")
def create_policy(car_id: int):
    session = get_session()

    try:
        payload = PolicyIn.model_validate(request.get_json() or {})
    except ExceptionGroup as e:
        return jsonify({"error": "Invalid payload", "detail": str(e)}), 400
    
    try:
        p = create_policy_for_car(
            session = session,
            car_id = car_id,
            provider = payload.provider,
            start_date = payload.startDate,
            end_date = payload.endDate,
        )
    except ValidationError as ve:
        return jsonify({"error": str(ve)}), 400
    except NotFoundError as nf:
        return jsonify({"error": str(nf)}), 404
    
    location = f"/api/cars/{car_id}/policies/{p.id}"
    resp = jsonify({
        "id": p.id,
        "carId": p.car_id,
        "provider": p.provider,
        "startDate": p.start_date.isoformat(),
        "endDate": p.end_date.isoformat(),
    })
    resp.status_code = 201
    resp.headers["Location"] = location
    return resp
