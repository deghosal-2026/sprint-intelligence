from flask import Blueprint, jsonify

bp = Blueprint("admin", __name__, url_prefix="/api/admin")


@bp.route("/system")
def system():
    return jsonify({
        "db": "disconnected",
        "ollama": "disconnected",
        "github_remaining": None,
    })
