from flask import Blueprint, jsonify, request

bp = Blueprint("ask", __name__, url_prefix="/api/ask")


@bp.route("", methods=["POST"])
def ask():
    data = request.get_json() or {}
    return jsonify({
        "answer": "Not implemented yet.",
        "model_used": None,
    })
