from flask import Blueprint, jsonify
from werkzeug.exceptions import HTTPException
from app.services.policy_service import ValidationError, NotFoundError as PolicyNotFound
from app.services.claim_service import ValidationError as ClaimValidation, NotFoundError as ClaimNotFound
from app.services.validity_service import NotFoundError as ValidityNotFound
from structlog import get_logger

blp = Blueprint("errors", __name__)

@blp.app_errorhandler(HTTPException)
def handle_http(e: HTTPException):
    return jsonify({"detail": e.description}), e.code

@blp.app_errorhandler(PolicyNotFound)
@blp.app_errorhandler(ClaimNotFound)
@blp.app_errorhandler(ValidityNotFound)
def handle_not_found(e):
    return jsonify({"detail": "Resource not found"}), 404

@blp.app_errorhandler(ClaimValidation)
@blp.app_errorhandler(ValidationError)
def handle_validation(e):
    return jsonify({"error": str(e)}), 400

@blp.app_errorhandler(Exception)
def handle_500(e):
    get_logger().exception("unhandled_error", err=str(e))
    return jsonify({"detail": "Internal Server Error"}), 500
