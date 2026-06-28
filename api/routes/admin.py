"""Admin API endpoints — system status, poller status, AI summary management."""

from flask import Blueprint, jsonify, request
from api.models import db, AISummary
from api.poller import github_client as gh, ollama_client as llm
from api.poller.compute import generate_ai_summaries
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

    gh_remaining = gh.get_rate_limit_remaining()
    llm_ok = llm.is_available()

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
    persona = request.args.get("persona", "sdm")
    results = generate_ai_summaries(persona=persona)
    return jsonify({"status": "ok", **results})
