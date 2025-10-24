from flask import Blueprint, jsonify
from app.db.session import get_session
from app.services.history_service import get_car_history, NotFoundError

blp = Blueprint("history", __name__)

@blp.get("/api/cars/<int:car_id>/history")
def car_history(car_id: int):
    session = get_session()

    try:
        events = get_car_history(session, car_id)
    except NotFoundError:
        return jsonify({"detail": "Car not found"}), 404

    return jsonify(events), 200
