from flask import Blueprint, request, jsonify

from app.db.session import get_session
from app.db.repositories import get_cars_with_owner
from app.api.schemas import CarOut

blp = Blueprint("cars", __name__)

@blp.route("/api/cars")
def get_cars():
    session = get_session()
    cars = get_cars_with_owner(session)

    data = []

    for c in cars:
        item = CarOut(
            id = c.id,
            vin = c.vin,
            make = c.make,
            model = c.model,
            year_of_manufacture = c.year_of_manufacture,
            owner = { "id": c.owner.id, "name": c.owner.name , "email": c.owner.email },
        ).model_dump(by_alias=True)
        data.append(item)

    return jsonify(data), 200
    