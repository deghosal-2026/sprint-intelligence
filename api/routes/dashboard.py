"""Dashboard API endpoints — metrics, sprints, engineers."""

from flask import Blueprint, jsonify, request
from api.models import (
    Sprint, SprintMetric, EngineerSprintMetric, IssueSprintMap,
    Issue, Repo, Alert, db,
)

bp = Blueprint("dashboard", __name__, url_prefix="/api")


@bp.route("/health")
def health():
    try:
        db.session.execute(db.text("SELECT 1"))
        return jsonify({"status": "ok", "db": "connected"})
    except Exception as e:
        return jsonify({"status": "error", "db": str(e)}), 500


@bp.route("/sprints")
def list_sprints():
    sprints = Sprint.query.order_by(Sprint.start_date.desc()).all()
    return jsonify([
        {"id": s.id, "name": s.name, "start_date": s.start_date.isoformat(),
         "end_date": s.end_date.isoformat()}
        for s in sprints
    ])


@bp.route("/metrics/<int:sprint_id>")
def sprint_metrics(sprint_id):
    metric = SprintMetric.query.filter_by(sprint_id=sprint_id).first()
    if not metric:
        return jsonify({"error": "No metrics for sprint"}), 404
    return jsonify({
        "sprint_id": sprint_id,
        "planned_points": float(metric.planned_points) if metric.planned_points else 0,
        "completed_points": float(metric.completed_points) if metric.completed_points else 0,
        "velocity_ratio": float(metric.velocity_ratio) if metric.velocity_ratio else 0,
        "carry_over_points": float(metric.carry_over_points) if metric.carry_over_points else 0,
        "cycle_time_mean_hours": float(metric.cycle_time_mean_hours) if metric.cycle_time_mean_hours else None,
        "cycle_time_median_hours": float(metric.cycle_time_median_hours) if metric.cycle_time_median_hours else None,
        "cycle_time_p90_hours": float(metric.cycle_time_p90_hours) if metric.cycle_time_p90_hours else None,
        "total_prs_merged": metric.total_prs_merged or 0,
        "bugs_introduced": metric.bugs_introduced or 0,
        "bugs_closed": metric.bugs_closed or 0,
        "bug_regression_rate": float(metric.bug_regression_rate) if metric.bug_regression_rate else 0,
        "planned_capacity": float(metric.planned_capacity) if metric.planned_capacity else 0,
        "actual_capacity": float(metric.actual_capacity) if metric.actual_capacity else 0,
        "capacity_ratio": float(metric.capacity_ratio) if metric.capacity_ratio else 0,
        "deploy_frequency": float(metric.deploy_frequency) if metric.deploy_frequency else None,
        "lead_time_hours": float(metric.lead_time_hours) if metric.lead_time_hours else None,
        "mttr_hours": float(metric.mttr_hours) if metric.mttr_hours else None,
        "change_failure_rate": float(metric.change_failure_rate) if metric.change_failure_rate else None,
    })


@bp.route("/metrics/<int:sprint_id>/engineers")
def engineer_metrics(sprint_id):
    metrics = EngineerSprintMetric.query.filter_by(sprint_id=sprint_id).all()
    return jsonify([
        {
            "engineer": m.engineer_login,
            "completed_points": float(m.completed_points) if m.completed_points else 0,
            "story_count": m.story_count or 0,
            "prs_merged": m.prs_merged or 0,
            "cycle_time_mean_hours": float(m.cycle_time_mean_hours) if m.cycle_time_mean_hours else None,
            "prs_reviewed": m.prs_reviewed or 0,
            "max_concurrent_issues": m.max_concurrent_issues or 0,
            "blocked_count": m.blocked_count or 0,
        }
        for m in metrics
    ])


@bp.route("/metrics/<int:sprint_id>/trend")
def sprint_trend(sprint_id):
    sprint = Sprint.query.get(sprint_id)
    if not sprint:
        return jsonify({"error": "Sprint not found"}), 404

    repo = Repo.query.get(sprint.repo_id)
    team_sprints = Sprint.query.filter_by(repo_id=repo.id).order_by(
        Sprint.start_date.desc()
    ).limit(6).all() if repo else [sprint]

    trends = []
    for s in team_sprints:
        metric = SprintMetric.query.filter_by(sprint_id=s.id).first()
        if metric:
            trends.append({
                "sprint": s.name,
                "start_date": s.start_date.isoformat(),
                "planned_points": float(metric.planned_points) if metric.planned_points else 0,
                "completed_points": float(metric.completed_points) if metric.completed_points else 0,
                "velocity_ratio": float(metric.velocity_ratio) if metric.velocity_ratio else 0,
                "cycle_time_mean_hours": float(metric.cycle_time_mean_hours) if metric.cycle_time_mean_hours else None,
                "bugs_introduced": metric.bugs_introduced or 0,
                "bugs_closed": metric.bugs_closed or 0,
            })

    return jsonify(trends)


@bp.route("/alerts")
def list_alerts():
    sprint_id = request.args.get("sprint_id", type=int)
    query = Alert.query
    if sprint_id:
        query = query.filter_by(sprint_id=sprint_id)
    alerts = query.order_by(Alert.created_at.desc()).limit(50).all()
    return jsonify([
        {
            "id": a.id,
            "type": a.alert_type,
            "severity": a.severity,
            "title": a.title,
            "description": a.description,
            "engineer_login": a.engineer_login,
            "created_at": a.created_at.isoformat() if a.created_at else None,
        }
        for a in alerts
    ])

