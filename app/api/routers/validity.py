from flask import Blueprint, request, jsonify
from app.db.session import get_session
from app.api.schemas import ValidityQuery
from app.services.validity_service import is_car_insured_on_date, NotFoundError

blp = Blueprint("validity", __name__)

@blp.get("/api/cars/<int:car_id>/insurance-valid")
def insurance_valid(car_id: int):

    if "date" not in request.args:
        return jsonify({"error": "query param 'date' is required (YYYY-MM-DD)"}), 400
    try:
        q = ValidityQuery.model_validate({"date": request.args.get("date")})
    except Exception as e:
        return jsonify({"error": "Invalid 'date' query param", "detail": str(e)}), 400

    session = get_session()
    try:
        valid = is_car_insured_on_date(session, car_id, q.date)
    except NotFoundError:
        return jsonify({"detail": "Car not found"}), 404

    return jsonify({
        "carId": car_id,
        "date": q.date.isoformat(),
        "valid": bool(valid),
    }), 200
