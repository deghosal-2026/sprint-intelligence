"""Phase 2: Compute sprint metrics, engineer metrics, AI summaries, DORA, and risk alerts."""

import statistics
from datetime import datetime, timedelta
from api.models import (
    Repo, Issue, PullRequest, Sprint, IssueSprintMap,
    SprintMetric, EngineerSprintMetric, AISummary, DeployEvent, Incident,
    Alert, Threshold, TeamForecast, db,
)
from . import ollama_client as llm
from . import prompts


def iso_week_range(year, week_start, num_sprints=12):
    sprints = []
    for i in range(num_sprints):
        sw = week_start + i * 2
        ew = sw + 1
        start = datetime.strptime(f"{year}-W{sw:02d}-1", "%Y-W%W-%w").date()
        end = start + timedelta(days=13)
        sprints.append({
            "name": f"{year}.{sw:02d}.{ew:02d}",
            "start_date": start,
            "end_date": end,
            "source_type": "synthetic",
        })
    return sprints


def resolve_sprints():
    from . import config as cfg
    cfg.sync_config()

    repos = Repo.query.all()
    sprint_map = {}

    for repo in repos:
        team_name = repo.team or f"repo-{repo.id}"
        sprints = iso_week_range(2026, 2, 12)

        for sp in sprints:
            full_name = f"{team_name}-{sp['name']}"
            existing = Sprint.query.filter_by(name=full_name).first()
            if existing:
                sprint_map[full_name] = existing.id
                continue

            sprint = Sprint(
                name=full_name,
                start_date=sp["start_date"],
                end_date=sp["end_date"],
                source_type=sp["source_type"],
                repo_id=repo.id,
            )
            db.session.add(sprint)
            db.session.flush()
            sprint_map[full_name] = sprint.id

    db.session.commit()
    return sprint_map


def find_sprint_for_issue(issue, sprints, team_name):
    if issue.milestone_title:
        for name, sp in sprints.items():
            if name.startswith(team_name):
                return sp
    if issue.created_at:
        c_date = issue.created_at.date() if hasattr(issue.created_at, "date") else issue.created_at
        for name, sp_id in sprints.items():
            if not name.startswith(team_name):
                continue
            sprint = Sprint.query.get(sp_id)
            if sprint and sprint.start_date <= c_date <= sprint.end_date:
                return sp_id
    return None


def map_issues_to_sprints():
    sprint_map = {s.name: s.id for s in Sprint.query.all()}
    repos = Repo.query.all()
    mapped = 0

    for repo in repos:
        team_name = repo.team or f"repo-{repo.id}"
        issues = Issue.query.filter_by(repo_id=repo.id).all()

        for issue in issues:
            sprint_id = find_sprint_for_issue(issue, sprint_map, team_name)
            if not sprint_id:
                continue

            existing = IssueSprintMap.query.filter_by(
                issue_id=issue.id, sprint_id=sprint_id
            ).first()
            if not existing:
                db.session.add(IssueSprintMap(issue_id=issue.id, sprint_id=sprint_id))
                mapped += 1

    db.session.commit()
    return mapped


def compute_sprint_metrics():
    sprints = Sprint.query.all()
    results = []

    for sprint in sprints:
        issue_ids = [
            row.issue_id
            for row in IssueSprintMap.query.filter_by(sprint_id=sprint.id).all()
        ]
        sprint_issues = Issue.query.filter(Issue.id.in_(issue_ids)).all() if issue_ids else []

        prs = PullRequest.query.filter(
            PullRequest.repo_id == sprint.repo_id,
            PullRequest.merged_at.isnot(None),
            PullRequest.merged_at >= sprint.start_date.isoformat(),
            PullRequest.merged_at <= (sprint.end_date + timedelta(days=1)).isoformat(),
        ).all()

        planned = sum(i.story_points or 0 for i in sprint_issues)
        completed = sum(i.story_points or 0 for i in sprint_issues if i.state == "closed")
        velocity_ratio = round(completed / planned, 4) if planned else None
        carry_over = sum(i.story_points or 0 for i in sprint_issues if i.state == "open")

        cycle_times = [
            pr.cycle_time_hours for pr in prs
            if pr.cycle_time_hours is not None
        ]
        ct_mean = round(statistics.mean(cycle_times), 2) if cycle_times else None
        ct_median = round(statistics.median(cycle_times), 2) if cycle_times else None
        ct_p90 = None
        if cycle_times:
            sorted_ct = sorted(cycle_times)
            idx = int(len(sorted_ct) * 0.9)
            ct_p90 = round(sorted_ct[min(idx, len(sorted_ct) - 1)], 2)

        bugs_intro = sum(
            1 for i in sprint_issues
            if i.is_bug and i.created_at
            and sprint.start_date <= i.created_at.date() <= sprint.end_date
        )
        bugs_closed = sum(
            1 for i in sprint_issues
            if i.is_bug and i.closed_at
            and sprint.start_date <= i.closed_at.date() <= sprint.end_date
        )
        bug_rate = round(bugs_intro / completed, 4) if completed else None

        existing = SprintMetric.query.filter_by(sprint_id=sprint.id).first()
        if existing:
            metric = existing
        else:
            metric = SprintMetric(sprint_id=sprint.id)
            db.session.add(metric)

        metric.planned_points = planned
        metric.completed_points = completed
        metric.velocity_ratio = velocity_ratio
        metric.carry_over_points = carry_over
        metric.cycle_time_mean_hours = ct_mean
        metric.cycle_time_median_hours = ct_median
        metric.cycle_time_p90_hours = ct_p90
        metric.total_prs_merged = len(prs)
        metric.bugs_introduced = bugs_intro
        metric.bugs_closed = bugs_closed
        metric.bug_regression_rate = bug_rate
        metric.planned_capacity = planned
        metric.actual_capacity = completed
        metric.capacity_ratio = velocity_ratio
        metric.computed_at = datetime.utcnow()

        results.append({
            "sprint": sprint.name,
            "planned": planned,
            "completed": completed,
            "velocity_ratio": velocity_ratio,
        })

    db.session.commit()
    return results


def compute_engineer_metrics():
    sprints = Sprint.query.all()
    results = []

    for sprint in sprints:
        issue_ids = [
            row.issue_id
            for row in IssueSprintMap.query.filter_by(sprint_id=sprint.id).all()
        ]
        sprint_issues = Issue.query.filter(Issue.id.in_(issue_ids)).all() if issue_ids else []

        engineers = set(i.assignee_login for i in sprint_issues if i.assignee_login)

        for eng in engineers:
            eng_issues = [i for i in sprint_issues if i.assignee_login == eng]
            completed = sum(i.story_points or 0 for i in eng_issues if i.state == "closed")

            prs = PullRequest.query.filter(
                PullRequest.author_login == eng,
                PullRequest.merged_at.isnot(None),
            ).all()
            prs_in_sprint = [
                p for p in prs
                if p.merged_at
                and sprint.start_date <= p.merged_at.date() <= sprint.end_date
            ]
            ct_values = [
                p.cycle_time_hours for p in prs_in_sprint
                if p.cycle_time_hours is not None
            ]

            reviews = PullRequest.query.filter(
                PullRequest.reviewers.any(eng),
            ).all()
            reviews_in_sprint = [
                r for r in reviews
                if r.created_at
                and sprint.start_date <= r.created_at.date() <= sprint.end_date
            ]

            open_issues = [i for i in eng_issues if i.state == "open"]
            blocked = sum(1 for i in eng_issues if i.is_blocked)

            existing = EngineerSprintMetric.query.filter_by(
                sprint_id=sprint.id, engineer_login=eng
            ).first()
            if existing:
                em = existing
            else:
                em = EngineerSprintMetric(
                    sprint_id=sprint.id, engineer_login=eng
                )
                db.session.add(em)

            em.completed_points = completed
            em.story_count = len(eng_issues)
            em.prs_merged = len(prs_in_sprint)
            em.cycle_time_mean_hours = round(statistics.mean(ct_values), 2) if ct_values else None
            em.prs_reviewed = len(reviews_in_sprint)
            em.max_concurrent_issues = len(open_issues)
            em.avg_wip = round(len(open_issues), 1)
            em.blocked_count = blocked
            em.computed_at = datetime.utcnow()

            results.append({"engineer": eng, "sprint": sprint.name, "completed": completed})

    db.session.commit()
    return results


def detect_alerts():
    from . import config as cfg
    cfg.sync_config()

    Alert.query.delete()
    db.session.flush()

    stale_days = int(Threshold.query.filter_by(key="stale_pr_days").first().value or 3)
    max_wip = int(Threshold.query.filter_by(key="max_wip").first().value or 4)
    scope_creep_pts = int(Threshold.query.filter_by(key="scope_creep_points").first().value or 6)

    sprints = Sprint.query.all()
    alerts_created = 0

    now = datetime.utcnow()

    stale_prs = PullRequest.query.filter(
        PullRequest.state == "open",
        PullRequest.created_at < (now - timedelta(days=stale_days)),
    ).all()
    for pr in stale_prs:
        db.session.add(Alert(
            sprint_id=None,
            alert_type="stale_pr",
            severity="warning",
            title=f"Stale PR: {pr.title[:80]}",
            description=f"No activity in {stale_days}+ days",
            pr_id=pr.id,
        ))
        alerts_created += 1

    from sqlalchemy import func
    overloaded = (
        db.session.query(Issue.assignee_login, func.count(Issue.id))
        .filter(Issue.state == "open")
        .group_by(Issue.assignee_login)
        .having(func.count(Issue.id) > max_wip)
        .all()
    )
    for eng, wip in overloaded:
        db.session.add(Alert(
            sprint_id=None,
            alert_type="overloaded_engineer",
            severity="warning",
            title=f"Overloaded: {eng} (WIP: {wip})",
            description=f"Current WIP {wip} exceeds threshold of {max_wip}",
            engineer_login=eng,
            issue_count=wip,
        ))
        alerts_created += 1

    for sprint in sprints:
        issue_ids = [
            row.issue_id
            for row in IssueSprintMap.query.filter_by(sprint_id=sprint.id).all()
        ]
        if not issue_ids:
            continue
        late_issues = Issue.query.filter(
            Issue.id.in_(issue_ids),
            Issue.created_at > sprint.start_date.isoformat(),
        ).all()
        if late_issues:
            total_pts = sum(i.story_points or 0 for i in late_issues)
            if total_pts >= scope_creep_pts:
                db.session.add(Alert(
                    sprint_id=sprint.id,
                    alert_type="scope_creep",
                    severity="warning",
                    title=f"Scope creep in {sprint.name}",
                    description=f"{len(late_issues)} issues ({total_pts} pts) added after sprint start",
                    issue_count=len(late_issues),
                    points_added=total_pts,
                ))
                alerts_created += 1

    db.session.commit()
    return alerts_created


def _fetch_metric_dict(sprint_id):
    metric = SprintMetric.query.filter_by(sprint_id=sprint_id).first()
    if not metric:
        return {}
    return {
        "velocity_ratio": float(metric.velocity_ratio) if metric.velocity_ratio else None,
        "cycle_time_mean_hours": float(metric.cycle_time_mean_hours) if metric.cycle_time_mean_hours else None,
        "cycle_time_median_hours": float(metric.cycle_time_median_hours) if metric.cycle_time_median_hours else None,
        "bugs_introduced": metric.bugs_introduced or 0,
        "capacity_ratio": float(metric.capacity_ratio) if metric.capacity_ratio else None,
        "planned_points": float(metric.planned_points) if metric.planned_points else 0,
        "completed_points": float(metric.completed_points) if metric.completed_points else 0,
        "carry_over_points": float(metric.carry_over_points) if metric.carry_over_points else 0,
    }


def _generate_sdm_summary(sprint, results):
    existing = AISummary.query.filter_by(
        sprint_id=sprint.id, persona_level="sdm"
    ).first()
    if existing and existing.reviewed:
        results["skipped"] += 1
        return
    metrics = _fetch_metric_dict(sprint.id)
    if not metrics.get("velocity_ratio") and not metrics.get("cycle_time_mean_hours"):
        results["skipped"] += 1
        return
    prompt = prompts.sdm_summary_prompt(metrics)
    text = llm.chat(prompt, system=prompts.SDM_SUMMARY_SYSTEM)
    if text is None:
        results["errors"] += 1
        return
    if existing:
        existing.summary_text = text
    else:
        db.session.add(AISummary(
            sprint_id=sprint.id, persona_level="sdm",
            summary_text=text, model_used=llm.OMLX_MODEL,
        ))
    results["generated"] += 1


def _generate_srsdm_summary(results):
    sprint_id = None
    team_metrics = []
    repos = Repo.query.filter(Repo.team.isnot(None)).all()
    for repo in repos:
        latest = Sprint.query.filter_by(repo_id=repo.id).order_by(
            Sprint.start_date.desc()
        ).first()
        if not latest:
            continue
        if sprint_id is None:
            sprint_id = latest.id
        metrics = _fetch_metric_dict(latest.id)
        if metrics:
            metrics["team"] = repo.team
            team_metrics.append(metrics)

    if not team_metrics:
        return
    existing = AISummary.query.filter_by(
        sprint_id=sprint_id, persona_level="srsdm"
    ).first()
    if existing and existing.reviewed:
        results["skipped"] += 1
        return
    prompt = prompts.srsdm_summary_prompt(team_metrics)
    text = llm.chat(prompt, system=prompts.SRSDM_SUMMARY_SYSTEM)
    if text is None:
        results["errors"] += 1
        return
    if existing:
        existing.summary_text = text
    else:
        db.session.add(AISummary(
            sprint_id=sprint_id, persona_level="srsdm",
            summary_text=text, model_used=llm.OMLX_MODEL,
        ))
    results["generated"] += 1


def _generate_director_summary(results):
    repos = Repo.query.filter(Repo.team.isnot(None)).all()
    quarterly_data = []
    sprint_id = None
    for repo in repos:
        sprints = Sprint.query.filter_by(repo_id=repo.id).order_by(
            Sprint.start_date.desc()
        ).limit(12).all()
        if not sprints:
            continue
        if sprint_id is None:
            sprint_id = sprints[0].id
        sprint_ids = [s.id for s in sprints]
        metrics = SprintMetric.query.filter(
            SprintMetric.sprint_id.in_(sprint_ids)
        ).all()
        n = len(metrics)
        if n == 0:
            continue
        avg = lambda field: float(
            sum(getattr(m, field) for m in metrics if getattr(m, field) is not None) / n
        )
        last = _fetch_metric_dict(sprints[0].id)
        prev4 = SprintMetric.query.filter(
            SprintMetric.sprint_id.in_([s.id for s in sprints[4:8]])
        ).all()
        prev = lambda field: float(
            sum(getattr(m, field) for m in prev4 if getattr(m, field) is not None) / max(len(prev4), 1)
        ) if prev4 else None

        qoq = {}
        for key in ["velocity_ratio", "cycle_time_mean_hours"]:
            curr = last.get(key)
            p = prev(key)
            if curr is not None and p is not None and p != 0:
                qoq[key] = round((curr - p) / abs(p) * 100, 1)
            else:
                qoq[key] = None

        quarterly_data.append({
            "team": repo.team,
            "averages": {
                "velocity_ratio": avg("velocity_ratio"),
                "cycle_time_mean_hours": avg("cycle_time_mean_hours"),
            },
            "qoq_delta": qoq,
        })

    if not quarterly_data:
        return
    existing = AISummary.query.filter_by(
        sprint_id=sprint_id, persona_level="director"
    ).first()
    if existing and existing.reviewed:
        results["skipped"] += 1
        return
    prompt = prompts.director_summary_prompt(quarterly_data)
    text = llm.chat(prompt, system=prompts.DIRECTOR_SUMMARY_SYSTEM)
    if text is None:
        results["errors"] += 1
        return
    if existing:
        existing.summary_text = text
    else:
        db.session.add(AISummary(
            sprint_id=sprint_id, persona_level="director",
            summary_text=text, model_used=llm.OMLX_MODEL,
        ))
    results["generated"] += 1


def generate_all_summaries():
    results = {"sdm": {"generated": 0, "skipped": 0, "errors": 0},
               "srsdm": {"generated": 0, "skipped": 0, "errors": 0},
               "director": {"generated": 0, "skipped": 0, "errors": 0}}

    if not llm.is_available():
        return {"error": "LLM unavailable"}

    sprints = Sprint.query.order_by(Sprint.start_date.desc()).all()
    for sprint in sprints:
        _generate_sdm_summary(sprint, results["sdm"])

    _generate_srsdm_summary(results["srsdm"])
    _generate_director_summary(results["director"])

    db.session.commit()
    return results


def generate_ai_summaries(persona="sdm"):
    if persona == "all":
        return generate_all_summaries()
    return _generate_single_persona_summaries(persona)


def _generate_single_persona_summaries(persona):
    sprints = Sprint.query.order_by(Sprint.start_date.desc()).all()
    results = {"generated": 0, "skipped": 0, "errors": 0}

    if not llm.is_available():
        return {"generated": 0, "skipped": len(sprints), "errors": 0, "reason": "LLM unavailable"}

    for sprint in sprints:
        existing = AISummary.query.filter_by(
            sprint_id=sprint.id, persona_level=persona
        ).first()
        if existing and existing.reviewed:
            results["skipped"] += 1
            continue

        metrics = _fetch_metric_dict(sprint.id)
        if not metrics.get("velocity_ratio") and not metrics.get("cycle_time_mean_hours"):
            results["skipped"] += 1
            continue

        prompt = prompts.sdm_summary_prompt(metrics)
        system = prompts.SDM_SUMMARY_SYSTEM
        text = llm.chat(prompt, system=system)

        if text is None:
            results["errors"] += 1
            continue

        if existing:
            existing.summary_text = text
        else:
            db.session.add(AISummary(
                sprint_id=sprint.id,
                persona_level=persona,
                summary_text=text,
                model_used=llm.OMLX_MODEL,
            ))
        results["generated"] += 1

    db.session.commit()
    return results


def compute_forecasts():
    repos = Repo.query.filter(Repo.team.isnot(None)).all()
    results = []

    for repo in repos:
        sprints = Sprint.query.filter_by(repo_id=repo.id).order_by(
            Sprint.start_date.asc()
        ).limit(12).all()
        sprint_ids = [s.id for s in sprints]
        metrics = SprintMetric.query.filter(
            SprintMetric.sprint_id.in_(sprint_ids)
        ).order_by(SprintMetric.sprint_id).all()

        for field in ["velocity_ratio", "cycle_time_mean_hours", "bug_regression_rate",
                       "deploy_frequency", "change_failure_rate"]:
            values = [
                float(getattr(m, field))
                for m in metrics
                if getattr(m, field) is not None
            ]
            if len(values) < 3:
                continue

            n = len(values)
            x_mean = (n - 1) / 2
            y_mean = sum(values) / n
            numerator = sum((i - x_mean) * (v - y_mean) for i, v in enumerate(values))
            denominator = sum((i - x_mean) ** 2 for i in range(n))
            slope = numerator / denominator if denominator else 0
            intercept = y_mean - slope * x_mean
            forecast = intercept + slope * n
            current = values[-1]

            if slope > 0.01:
                direction = "increasing"
            elif slope < -0.01:
                direction = "decreasing"
            else:
                direction = "stable"

            existing = TeamForecast.query.filter_by(
                team=repo.team, metric=field
            ).first()
            if existing:
                fc = existing
            else:
                fc = TeamForecast(team=repo.team, metric=field)
                db.session.add(fc)

            fc.current_value = round(current, 4)
            fc.forecast_value = round(forecast, 4)
            fc.trend_direction = direction
            fc.slope = round(slope, 6)
            fc.computed_at = datetime.utcnow()

            results.append({
                "team": repo.team,
                "metric": field,
                "current": round(current, 4),
                "forecast": round(forecast, 4),
                "direction": direction,
                "slope": round(slope, 6),
            })

    db.session.commit()
    return results


def compute_dora_metrics():
    sprints = Sprint.query.all()
    results = []

    for sprint in sprints:
        deploys = DeployEvent.query.filter(
            DeployEvent.repo_id == sprint.repo_id,
            DeployEvent.deployed_at >= sprint.start_date.isoformat(),
            DeployEvent.deployed_at <= (sprint.end_date + timedelta(days=1)).isoformat(),
        ).all()

        total_deploys = len(deploys)
        sprint_weeks = max((sprint.end_date - sprint.start_date).days / 7, 1)
        deploy_freq = round(total_deploys / sprint_weeks, 2) if total_deploys else None

        lead_times = []
        for d in deploys:
            prs = PullRequest.query.filter(
                PullRequest.repo_id == d.repo_id,
                PullRequest.merged_at.isnot(None),
                PullRequest.merged_at <= d.deployed_at,
            ).order_by(PullRequest.merged_at.desc()).limit(5).all()
            for pr in prs:
                if pr.first_commit_at and pr.merged_at:
                    lt = (pr.merged_at - pr.first_commit_at).total_seconds() / 3600
                    lead_times.append(lt)
        lead_time = round(statistics.mean(lead_times), 2) if lead_times else None

        incidents = Incident.query.filter(
            Incident.created_at >= sprint.start_date.isoformat(),
            Incident.created_at <= (sprint.end_date + timedelta(days=1)).isoformat(),
        ).all()

        mttr_values = [i.mttr_hours for i in incidents if i.mttr_hours is not None]
        mttr = round(statistics.mean(mttr_values), 2) if mttr_values else None

        failed = sum(1 for i in incidents if i.is_change_failure)
        cfr = round(failed / total_deploys, 4) if total_deploys else None

        metric = SprintMetric.query.filter_by(sprint_id=sprint.id).first()
        if not metric:
            metric = SprintMetric(sprint_id=sprint.id)
            db.session.add(metric)

        metric.deploy_frequency = deploy_freq
        metric.lead_time_hours = lead_time
        metric.mttr_hours = mttr
        metric.change_failure_rate = cfr

        results.append({
            "sprint": sprint.name,
            "deploy_frequency": deploy_freq,
            "lead_time_hours": lead_time,
            "mttr_hours": mttr,
            "change_failure_rate": cfr,
        })

    db.session.commit()
    return results
