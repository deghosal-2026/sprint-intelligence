"""Admin API endpoints — system status, poller status."""

import os
import requests as http_requests
from flask import Blueprint, jsonify
from api.models import db
from api.poller import github_client as gh
from api.routes.poller import POLLER_STATUS

bp = Blueprint("admin", __name__, url_prefix="/api/admin")


@bp.route("/system")
def system():
    db_ok = False
    try:
        db.session.execute(db.text("SELECT 1"))
        db_ok = True
    except Exception:
        pass

    ollama_url = os.getenv("OLLAMA_URL", "http://host.docker.internal:11434")
    ollama_ok = False
    try:
        r = http_requests.get(f"{ollama_url}/api/tags", timeout=5)
        ollama_ok = r.status_code == 200
    except Exception:
        pass

    gh_remaining = gh.get_rate_limit_remaining()

    return jsonify({
        "db": "connected" if db_ok else "disconnected",
        "ollama": "connected" if ollama_ok else "disconnected",
        "github_remaining": gh_remaining,
        "poller": POLLER_STATUS,
    })
