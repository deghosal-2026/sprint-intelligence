"""Poller trigger endpoints — wraps Phase 1 and Phase 2."""

from flask import Blueprint, jsonify
from api.models import db

bp = Blueprint("poller", __name__, url_prefix="/api/poller")

POLLER_STATUS = {"status": "idle", "last_fetch": None, "last_compute": None}


def _run_phase1():
    from api.poller.fetch import run_fetch
    return run_fetch()


def _run_phase2():
    from api.poller.compute import (
        resolve_sprints, map_issues_to_sprints,
        compute_sprint_metrics, compute_engineer_metrics,
        compute_dora_metrics, detect_alerts, compute_forecasts,
        generate_all_summaries,
    )
    sprint_map = resolve_sprints()
    mapped = map_issues_to_sprints()
    metrics = compute_sprint_metrics()
    eng_metrics = compute_engineer_metrics()
    dora = compute_dora_metrics()
    alerts = detect_alerts()
    compute_forecasts()
    ai_results = generate_all_summaries()
    return {
        "sprints": len(sprint_map),
        "issues_mapped": mapped,
        "sprint_metrics": len(metrics),
        "engineer_metrics": len(eng_metrics),
        "dora_metrics": len(dora),
        "alerts": alerts,
        "ai_summaries": ai_results,
    }


@bp.route("/status")
def status():
    return jsonify(POLLER_STATUS)


@bp.route("/fetch", methods=["POST"])
def fetch():
    POLLER_STATUS["status"] = "running"
    try:
        results = _run_phase1()
        total_issues = sum(r["issues"] for r in results.values())
        total_prs = sum(r["prs"] for r in results.values())
        POLLER_STATUS.update({
            "status": "idle",
            "last_fetch": str(db.session.execute(db.text("SELECT NOW()")).scalar()),
        })
        return jsonify({
            "status": "completed",
            "repos": len(results),
            "issues": total_issues,
            "prs": total_prs,
            "details": results,
        })
    except Exception as e:
        POLLER_STATUS["status"] = "error"
        return jsonify({"status": "error", "message": str(e)}), 500


@bp.route("/compute", methods=["POST"])
def compute():
    POLLER_STATUS["status"] = "running"
    try:
        results = _run_phase2()
        POLLER_STATUS.update({
            "status": "idle",
            "last_compute": str(db.session.execute(db.text("SELECT NOW()")).scalar()),
        })
        return jsonify({"status": "completed", **results})
    except Exception as e:
        POLLER_STATUS["status"] = "error"
        return jsonify({"status": "error", "message": str(e)}), 500


@bp.route("/full", methods=["POST"])
def full():
    POLLER_STATUS["status"] = "running"
    try:
        f1 = _run_phase1()
        f2 = _run_phase2()
        POLLER_STATUS.update({
            "status": "idle",
            "last_fetch": str(db.session.execute(db.text("SELECT NOW()")).scalar()),
            "last_compute": str(db.session.execute(db.text("SELECT NOW()")).scalar()),
        })
        total_issues = sum(r["issues"] for r in f1.values())
        total_prs = sum(r["prs"] for r in f1.values())
        return jsonify({
            "status": "completed",
            "phase1": {"repos": len(f1), "issues": total_issues, "prs": total_prs},
            "phase2": f2,
        })
    except Exception as e:
        POLLER_STATUS["status"] = "error"
        return jsonify({"status": "error", "message": str(e)}), 500
