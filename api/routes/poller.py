from flask import Blueprint, jsonify

bp = Blueprint("poller", __name__, url_prefix="/api/poller")


@bp.route("/status")
def status():
    return jsonify({"status": "idle", "last_fetch": None, "last_compute": None})


@bp.route("/fetch", methods=["POST"])
def fetch():
    return jsonify({"status": "not_implemented"})


@bp.route("/compute", methods=["POST"])
def compute():
    return jsonify({"status": "not_implemented"})


@bp.route("/full", methods=["POST"])
def full():
    return jsonify({"status": "not_implemented"})
