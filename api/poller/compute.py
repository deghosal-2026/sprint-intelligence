"""Phase 2: Compute sprint metrics, engineer metrics, and detect risk alerts."""

import statistics
from datetime import datetime, date, timedelta
from api.models import (
    Repo, Issue, PullRequest, Sprint, IssueSprintMap,
    SprintMetric, EngineerSprintMetric, Alert, Threshold, db,
)


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
            em.blocked_count = blocked
            em.computed_at = datetime.utcnow()

            results.append({"engineer": eng, "sprint": sprint.name, "completed": completed})

    db.session.commit()
    return results


def detect_alerts():
    from . import config as cfg
    cfg.sync_config()

    stale_days = int(Threshold.query.filter_by(key="stale_pr_days").first().value or 3)
    max_wip = int(Threshold.query.filter_by(key="max_wip").first().value or 4)
    scope_creep_pts = int(Threshold.query.filter_by(key="scope_creep_points").first().value or 6)

    sprints = Sprint.query.all()
    alerts_created = 0

    now = datetime.utcnow()

    stale_prs = PullRequest.query.filter(
        PullRequest.state == "open",
        PullRequest.updated_at < (now - timedelta(days=stale_days)),
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
