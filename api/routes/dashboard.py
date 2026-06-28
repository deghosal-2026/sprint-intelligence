"""Dashboard API endpoints — metrics, sprints, engineers, teams, quarterly."""

from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request
from sqlalchemy import func, case
from api.models import (
    Sprint, SprintMetric, EngineerSprintMetric, IssueSprintMap, AISummary,
    Issue, Repo, Alert, db,
)

bp = Blueprint("dashboard", __name__, url_prefix="/api")


def _repo_to_team(repo):
    """Get team name from a Repo row."""
    return repo.team or repo.name


def _sprint_metric_dict(metric):
    if not metric:
        return None
    return {
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
    }


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
    return jsonify({"sprint_id": sprint_id, **_sprint_metric_dict(metric)})


@bp.route("/teams")
def list_teams():
    repos = Repo.query.filter(Repo.team.isnot(None)).order_by(Repo.team).all()
    result = []
    for repo in repos:
        latest_sprint = Sprint.query.filter_by(repo_id=repo.id).order_by(
            Sprint.start_date.desc()
        ).first()
        result.append({
            "team": repo.team,
            "owner": repo.owner,
            "repo": repo.name,
            "latest_sprint_id": latest_sprint.id if latest_sprint else None,
            "latest_sprint_name": latest_sprint.name if latest_sprint else None,
        })
    return jsonify(result)


@bp.route("/quarterly")
def quarterly_aggregates():
    repos = Repo.query.filter(Repo.team.isnot(None)).order_by(Repo.team).all()
    result = []
    for repo in repos:
        sprints = Sprint.query.filter_by(repo_id=repo.id).order_by(
            Sprint.start_date.desc()
        ).limit(12).all()
        if not sprints:
            continue
        sprint_ids = [s.id for s in sprints]
        metrics = SprintMetric.query.filter(
            SprintMetric.sprint_id.in_(sprint_ids)
        ).all()
        n = len(metrics)
        avg = lambda field: float(
            sum(getattr(m, field) for m in metrics if getattr(m, field) is not None) / n
        ) if n > 0 else None

        last = _sprint_metric_dict(
            SprintMetric.query.filter_by(sprint_id=sprints[0].id).first()
        )
        prev4 = SprintMetric.query.filter(
            SprintMetric.sprint_id.in_([s.id for s in sprints[4:8]])
        ).all()
        prev_avg = lambda field: float(
            sum(getattr(m, field) for m in prev4 if getattr(m, field) is not None) / max(len(prev4), 1)
        ) if prev4 else None

        qoq_delta = {}
        if last and prev4:
            for key in ["velocity_ratio", "cycle_time_mean_hours", "bug_regression_rate",
                         "deploy_frequency", "lead_time_hours", "change_failure_rate"]:
                curr = last.get(key)
                prev = prev_avg(key)
                if curr is not None and prev is not None and prev != 0:
                    qoq_delta[key] = round((curr - prev) / abs(prev) * 100, 1)
                else:
                    qoq_delta[key] = None

        result.append({
            "team": repo.team,
            "quarter_sprints": len(sprints),
            "sprint_ids": sprint_ids,
            "quarter_start": sprints[-1].start_date.isoformat() if sprints else None,
            "quarter_end": sprints[0].end_date.isoformat() if sprints else None,
            "averages": {
                "velocity_ratio": avg("velocity_ratio"),
                "cycle_time_mean_hours": avg("cycle_time_mean_hours"),
                "total_prs_merged": avg("total_prs_merged"),
                "bugs_introduced": int(avg("bugs_introduced") or 0),
                "capacity_ratio": avg("capacity_ratio"),
                "deploy_frequency": avg("deploy_frequency"),
                "lead_time_hours": avg("lead_time_hours"),
                "change_failure_rate": avg("change_failure_rate"),
            },
            "qoq_delta": qoq_delta,
        })
    return jsonify(result)


@bp.route("/quarterly/org")
def quarterly_org():
    repos = Repo.query.filter(Repo.team.isnot(None)).order_by(Repo.team).all()
    all_sprints = []
    for repo in repos:
        sprints = Sprint.query.filter_by(repo_id=repo.id).order_by(
            Sprint.start_date.desc()
        ).limit(12).all()
        all_sprints.extend(sprints)
    all_sprints.sort(key=lambda s: s.start_date, reverse=True)
    all_sprints = all_sprints[:12]
    if not all_sprints:
        return jsonify({"error": "No data"}), 404

    sprint_ids = [s.id for s in all_sprints]
    metrics = SprintMetric.query.filter(
        SprintMetric.sprint_id.in_(sprint_ids)
    ).all()
    n = len(metrics)
    if n == 0:
        return jsonify({"error": "No metrics"}), 404

    avg = lambda field: float(
        sum(getattr(m, field) for m in metrics if getattr(m, field) is not None) / n
    )

    return jsonify({
        "quarter_sprints": len(all_sprints),
        "quarter_start": all_sprints[-1].start_date.isoformat(),
        "quarter_end": all_sprints[0].end_date.isoformat(),
        "averages": {
            "velocity_ratio": avg("velocity_ratio"),
            "cycle_time_mean_hours": avg("cycle_time_mean_hours"),
            "total_prs_merged": int(avg("total_prs_merged") or 0),
            "bugs_introduced": int(avg("bugs_introduced") or 0),
            "capacity_ratio": avg("capacity_ratio"),
            "deploy_frequency": avg("deploy_frequency"),
            "lead_time_hours": avg("lead_time_hours"),
            "change_failure_rate": avg("change_failure_rate"),
        },
    })


@bp.route("/patterns")
def cross_team_patterns():
    repos = Repo.query.filter(Repo.team.isnot(None)).order_by(Repo.team).all()
    patterns = {"slowdowns": [], "correlations": []}

    team_trends = {}
    for repo in repos:
        sprints = Sprint.query.filter_by(repo_id=repo.id).order_by(
            Sprint.start_date.asc()
        ).limit(12).all()
        sprint_ids = [s.id for s in sprints]
        metrics = SprintMetric.query.filter(
            SprintMetric.sprint_id.in_(sprint_ids)
        ).order_by(SprintMetric.sprint_id).all()

        velocities = []
        cycle_times = []
        for m in metrics:
            if m.velocity_ratio is not None:
                velocities.append(float(m.velocity_ratio))
            if m.cycle_time_mean_hours is not None:
                cycle_times.append(float(m.cycle_time_mean_hours))

        team_trends[repo.team] = {"velocities": velocities, "cycle_times": cycle_times}

        if len(velocities) >= 4:
            recent_avg = sum(velocities[-2:]) / 2
            early_avg = sum(velocities[:2]) / 2
            if early_avg > 0 and (early_avg - recent_avg) / early_avg > 0.3:
                patterns["slowdowns"].append({
                    "team": repo.team,
                    "decline_pct": round((early_avg - recent_avg) / early_avg * 100, 1),
                    "early_avg": round(early_avg, 3),
                    "recent_avg": round(recent_avg, 3),
                    "type": "velocity_decline",
                })

        if len(cycle_times) >= 4:
            recent_ct = sum(cycle_times[-2:]) / 2
            early_ct = sum(cycle_times[:2]) / 2
            if early_ct > 0 and (recent_ct - early_ct) / early_ct > 0.5:
                patterns["slowdowns"].append({
                    "team": repo.team,
                    "increase_pct": round((recent_ct - early_ct) / early_ct * 100, 1),
                    "early_avg": round(early_ct, 1),
                    "recent_avg": round(recent_ct, 1),
                    "type": "cycle_time_increase",
                })

    teams = list(team_trends.keys())
    for i in range(len(teams)):
        for j in range(i + 1, len(teams)):
            t1 = team_trends[teams[i]]
            t2 = team_trends[teams[j]]
            min_len = min(len(t1["velocities"]), len(t2["velocities"]))
            if min_len >= 3:
                v1 = t1["velocities"][-min_len:]
                v2 = t2["velocities"][-min_len:]
                diffs = sum(abs(a - b) for a, b in zip(v1, v2)) / min_len
                avg_vel = (sum(v1) + sum(v2)) / (min_len * 2)
                if avg_vel > 0 and diffs / avg_vel < 0.15:
                    patterns["correlations"].append({
                        "team_a": teams[i],
                        "team_b": teams[j],
                        "type": "velocity_correlation",
                        "avg_diff_pct": round(diffs / avg_vel * 100, 1),
                    })

    return jsonify(patterns)


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
            "avg_wip": float(m.avg_wip) if m.avg_wip else None,
            "avg_review_turnaround_hours": float(m.avg_review_turnaround_hours) if m.avg_review_turnaround_hours else None,
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


@bp.route("/metrics/<int:sprint_id>/summary")
def sprint_ai_summary(sprint_id):
    persona = request.args.get("persona", "sdm")
    if persona in ("srsdm", "director"):
        summary = AISummary.query.filter_by(persona_level=persona).order_by(
            AISummary.generated_at.desc()
        ).first()
    else:
        summary = AISummary.query.filter_by(
            sprint_id=sprint_id, persona_level=persona
        ).first()
    if not summary:
        return jsonify({"summary": None, "model_used": None})
    return jsonify({
        "summary": summary.summary_text,
        "model_used": summary.model_used,
        "generated_at": summary.generated_at.isoformat() if summary.generated_at else None,
        "reviewed": summary.reviewed,
    })

