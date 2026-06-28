"""Admin API endpoints — system status, poller status, AI summary management."""

from flask import Blueprint, jsonify
from api.models import db, AISummary
from api.poller import github_client as gh, ollama_client as llm
from api.routes.poller import POLLER_STATUS, _set_status, _background_job

bp = Blueprint("admin", __name__, url_prefix="/api/admin")


@bp.route("/system")
def system():
    db_ok = False
    try:
        db.session.execute(db.text("SELECT 1"))
        db_ok = True
    except Exception:
        pass

    try:
        gh_remaining = gh.get_rate_limit_remaining()
    except Exception:
        gh_remaining = None

    try:
        llm_ok = llm.is_available()
    except Exception:
        llm_ok = False

    return jsonify({
        "db": "connected" if db_ok else "disconnected",
        "ollama": "connected" if llm_ok else "disconnected",
        "github_remaining": gh_remaining,
        "poller": POLLER_STATUS,
    })


@bp.route("/summaries")
def list_summaries():
    summaries = AISummary.query.order_by(AISummary.generated_at.desc()).limit(50).all()
    return jsonify([
        {
            "id": s.id,
            "sprint_id": s.sprint_id,
            "persona_level": s.persona_level,
            "model_used": s.model_used,
            "generated_at": s.generated_at.isoformat() if s.generated_at else None,
            "reviewed": s.reviewed,
        }
        for s in summaries
    ])


@bp.route("/summaries/regenerate", methods=["POST"])
def regenerate_summaries():
    with __import__("threading").Lock():
        if POLLER_STATUS["status"] == "running":
            return jsonify({"status": "already_running"}), 409
        POLLER_STATUS["status"] = "running"
        POLLER_STATUS["progress"] = "Regenerating AI summaries..."
        POLLER_STATUS["error"] = None

    def _regen():
        from api.poller.compute import generate_all_summaries
        return generate_all_summaries()

    _background_job(_regen, "last_regenerate")
    return jsonify({"status": "started", "message": "Regenerating all summaries in background. Poll /api/poller/status for progress."})
