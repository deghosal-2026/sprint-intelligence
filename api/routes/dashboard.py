from flask import Blueprint, jsonify

bp = Blueprint("dashboard", __name__, url_prefix="/api")


@bp.route("/health")
def health():
    return jsonify({"status": "ok"})
