"""Poller trigger endpoints — wraps Phase 1 and Phase 2.

Heavy operations run in a background thread to avoid blocking gunicorn workers.
The frontend polls /api/poller/status for progress.
"""

import threading
import traceback
from flask import Blueprint, jsonify
from api.models import db

bp = Blueprint("poller", __name__, url_prefix="/api/poller")

POLLER_STATUS = {
    "status": "idle",
    "last_fetch": None,
    "last_compute": None,
    "last_regenerate": None,
    "progress": None,
    "error": None,
}

_lock = threading.Lock()


def _set_status(**kwargs):
    with _lock:
        POLLER_STATUS.update(kwargs)


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
    _set_status(progress="Resolving sprints...")
    sprint_map = resolve_sprints()
    _set_status(progress="Mapping issues to sprints...")
    mapped = map_issues_to_sprints()
    _set_status(progress="Computing sprint metrics...")
    metrics = compute_sprint_metrics()
    _set_status(progress="Computing engineer metrics...")
    eng_metrics = compute_engineer_metrics()
    _set_status(progress="Computing DORA metrics...")
    dora = compute_dora_metrics()
    _set_status(progress="Detecting alerts...")
    alerts = detect_alerts()
    _set_status(progress="Computing forecasts...")
    compute_forecasts()
    _set_status(progress="Generating AI summaries...")
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


def _run_regenerate():
    from api.poller.compute import generate_all_summaries
    return generate_all_summaries()


def _background_job(job_fn, success_key):
    app = None
    try:
        from flask import current_app
        app = current_app._get_current_object()
    except Exception:
        pass

    def _run():
        with app.app_context():
            try:
                results = job_fn()
                _set_status(status="idle", progress=None, error=None, **{success_key: str(results)})
            except Exception as e:
                tb = traceback.format_exc()
                print(f"[poller] Background job error: {e}\n{tb}", flush=True)
                _set_status(status="error", progress=None, error=str(e))

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()


@bp.route("/status")
def status():
    with _lock:
        return jsonify(dict(POLLER_STATUS))


@bp.route("/fetch", methods=["POST"])
def fetch():
    with _lock:
        if POLLER_STATUS["status"] == "running":
            return jsonify({"status": "already_running"}), 409
        POLLER_STATUS["status"] = "running"
        POLLER_STATUS["progress"] = "Starting fetch..."
        POLLER_STATUS["error"] = None
    _background_job(_run_phase1, "last_fetch")
    return jsonify({"status": "started", "message": "Fetch running in background. Poll /api/poller/status for progress."})


@bp.route("/compute", methods=["POST"])
def compute():
    with _lock:
        if POLLER_STATUS["status"] == "running":
            return jsonify({"status": "already_running"}), 409
        POLLER_STATUS["status"] = "running"
        POLLER_STATUS["progress"] = "Starting compute..."
        POLLER_STATUS["error"] = None
    _background_job(_run_phase2, "last_compute")
    return jsonify({"status": "started", "message": "Compute running in background. Poll /api/poller/status for progress."})


@bp.route("/full", methods=["POST"])
def full():
    with _lock:
        if POLLER_STATUS["status"] == "running":
            return jsonify({"status": "already_running"}), 409
        POLLER_STATUS["status"] = "running"
        POLLER_STATUS["progress"] = "Starting full poll..."
        POLLER_STATUS["error"] = None

    def _full():
        _run_phase1()
        _set_status(progress="Phase 1 done, starting Phase 2...")
        _run_phase2()

    _background_job(_full, "last_compute")
    return jsonify({"status": "started", "message": "Full poll running in background. Poll /api/poller/status for progress."})
