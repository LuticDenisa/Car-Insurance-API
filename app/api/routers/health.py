from flask import Blueprint, jsonify

blp = Blueprint("health", __name__)

@blp.get("/health")
def health():
    return jsonify({"status": "ok"}), 200
