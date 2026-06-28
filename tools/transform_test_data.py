"""Anonymize raw GitHub data, fabricate sprint structure, generate synthetic events."""

import hashlib
import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO_TEAM_MAP = {
    "microsoft/vscode": {"team": "team1", "engineers": 5},
    "facebook/react": {"team": "team2", "engineers": 5},
    "nodejs/node": {"team": "team3", "engineers": 5},
    "kubernetes/kubernetes": {"team": "team4", "engineers": 8},
    "rust-lang/rust": {"team": "team5", "engineers": 5},
    "vercel/next.js": {"team": "team6", "engineers": 4},
    "grafana/grafana": {"team": "team7", "engineers": 5},
    "angular/angular": {"team": "team8", "engineers": 4},
    "python/cpython": {"team": "team9", "engineers": 5},
    "tensorflow/tensorflow": {"team": "team10", "engineers": 4},
}

ISSUE_TYPES = ["feature", "feature", "feature", "bug", "bug", "tech-debt", "task"]
STORY_POINTS = [1, 2, 2, 3, 3, 3, 5, 5, 8, 13]


def _rng_for(github_id):
    seed = int(hashlib.md5(str(github_id).encode()).hexdigest()[:8], 16)
    return random.Random(seed)


def assign_properties(github_id):
    rng = _rng_for(github_id)
    issue_type = rng.choice(ISSUE_TYPES)
    points = rng.choice(STORY_POINTS)
    return issue_type, points


def build_engineer_map(contributors, team_name, count):
    contributor_set = sorted(set(c for c in contributors if c))
    seed = int(hashlib.md5(team_name.encode()).hexdigest()[:8], 16)
    rng = random.Random(seed)
    rng.shuffle(contributor_set)
    selected = contributor_set[:count]
    while len(selected) < count:
        selected.append(f"{team_name}-engineer{len(selected)+1}")
    return {
        real: f"{team_name}-engineer{i+1}"
        for i, real in enumerate(selected)
    }


def iso_week_range(year, week_start, num_sprints=12):
    sprints = []
    for i in range(num_sprints):
        sw = week_start + i * 2
        ew = sw + 1
        start = datetime.strptime(f"{year}-W{sw:02d}-1", "%Y-W%W-%w")
        end = start + timedelta(days=13, hours=23, minutes=59, seconds=59)
        sprints.append({
            "name": f"{year}.{sw:02d}.{ew:02d}",
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
            "start_week": sw,
            "end_week": ew,
        })
    return sprints


def process_repo(raw_dir, output_dir, repo_full, team_info):
    owner, repo_name = repo_full.split("/")
    team_name = team_info["team"]
    eng_count = team_info["engineers"]
    print(f"  Processing {repo_full} → {team_name}")

    issues_path = raw_dir / f"{owner}_{repo_name}_issues.json"
    pulls_path = raw_dir / f"{owner}_{repo_name}_pulls.json"
    milestones_path = raw_dir / f"{owner}_{repo_name}_milestones.json"

    if not issues_path.exists():
        print(f"    No issues file found, skipping")
        return None

    with open(issues_path) as f:
        raw_issues = json.load(f)
    with open(pulls_path) as f:
        raw_pulls = json.load(f)
    raw_milestones = []
    if milestones_path.exists():
        with open(milestones_path) as f:
            raw_milestones = json.load(f)

    all_contributors = []
    for issue in raw_issues:
        if issue.get("assignee") and issue["assignee"].get("login"):
            all_contributors.append(issue["assignee"]["login"])
        if issue.get("user") and issue["user"].get("login"):
            all_contributors.append(issue["user"]["login"])
    for pr in raw_pulls:
        if pr.get("user") and pr["user"].get("login"):
            all_contributors.append(pr["user"]["login"])

    eng_map = build_engineer_map(all_contributors, team_name, eng_count)
    reverse_map = {v: k for k, v in eng_map.items()}

    raw_dates = []
    for issue in raw_issues:
        if issue.get("created_at"):
            raw_dates.append(issue["created_at"])
    for pr in raw_pulls:
        if pr.get("created_at"):
            raw_dates.append(pr["created_at"])
    if not raw_dates:
        print(f"    No dates found, skipping")
        return None

    raw_dates.sort()
    earliest = datetime.fromisoformat(raw_dates[0].replace("Z", "+00:00"))
    latest = datetime.fromisoformat(raw_dates[-1].replace("Z", "+00:00"))

    ref_start = earliest.replace(tzinfo=None)
    ref_end = latest.replace(tzinfo=None)
    ref_span = (ref_end - ref_start).total_seconds()

    year = 2026
    week_start = 2
    sprints = iso_week_range(year, week_start, 12)
    sprint_start = datetime.fromisoformat(sprints[0]["start_date"])

    def shift_date(orig_iso):
        if not orig_iso:
            return None
        try:
            orig = datetime.fromisoformat(orig_iso.replace("Z", "+00:00")).replace(tzinfo=None)
        except ValueError:
            return None
        if ref_span <= 0:
            return sprint_start.isoformat()
        ratio = (orig - ref_start).total_seconds() / ref_span
        shifted = sprint_start + timedelta(seconds=ratio * 15552000)
        return shifted.isoformat()

    def map_to_engineer(login):
        if login in eng_map:
            return eng_map[login]
        return f"{team_name}-external-{hashlib.md5(login.encode()).hexdigest()[:6]}"

    transformed_issues = []
    for issue in raw_issues:
        gh_id = issue["id"]
        issue_type, points = assign_properties(gh_id)
        created = shift_date(issue.get("created_at"))
        closed = shift_date(issue.get("closed_at"))
        assignee = issue.get("assignee")
        assignee_login = map_to_engineer(assignee["login"]) if assignee and assignee.get("login") else None

        sprint_label = None
        for sprint in sprints:
            s_start = datetime.fromisoformat(sprint["start_date"])
            s_end = datetime.fromisoformat(sprint["end_date"])
            if created:
                c_dt = datetime.fromisoformat(created)
                if s_start <= c_dt <= s_end:
                    sprint_label = f"sprint:{team_name}-26.{sprint['start_week']:02d}.{sprint['end_week']:02d}"
                    break

        labels = issue.get("labels", [])
        label_names = [l.get("name", "") for l in labels] if labels else []
        is_blocked = "blocked" in label_names

        transformed_issues.append({
            "github_id": gh_id,
            "number": issue["number"],
            "title": issue.get("title", ""),
            "state": issue.get("state", "open"),
            "created_at": created,
            "closed_at": closed,
            "updated_at": shift_date(issue.get("updated_at")),
            "assignee_login": assignee_login,
            "story_points": points,
            "is_bug": issue_type == "bug",
            "is_feature": issue_type == "feature",
            "is_techdebt": issue_type == "tech-debt",
            "is_task": issue_type == "task",
            "is_blocked": is_blocked,
            "milestone_title": issue.get("milestone", {}).get("title") if issue.get("milestone") else None,
            "sprint_label": sprint_label,
            "created_after_sprint_start": False,
        })

    transformed_pulls = []
    for pr in raw_pulls:
        gh_id = pr["id"]
        created = shift_date(pr.get("created_at"))
        merged = shift_date(pr.get("merged_at"))
        closed = shift_date(pr.get("closed_at"))
        first_commit = pr.get("_first_commit_at")
        if first_commit:
            first_commit = shift_date(first_commit)

        cycle_time = None
        if first_commit and merged:
            try:
                fc = datetime.fromisoformat(first_commit.replace("Z", "+00:00") if "Z" in first_commit else first_commit)
                mg = datetime.fromisoformat(merged.replace("Z", "+00:00") if "Z" in merged else merged)
                cycle_time = round((mg - fc).total_seconds() / 3600, 2)
            except ValueError:
                pass

        author = pr.get("user", {})
        author_login = map_to_engineer(author.get("login")) if author else None

        raw_reviewers = pr.get("_reviewers", [])
        reviewers = [map_to_engineer(r) for r in raw_reviewers]

        transformed_pulls.append({
            "github_id": gh_id,
            "number": pr["number"],
            "title": pr.get("title", ""),
            "state": "merged" if pr.get("merged_at") else pr.get("state", "open"),
            "author_login": author_login,
            "created_at": created,
            "merged_at": merged,
            "closed_at": closed,
            "first_commit_at": first_commit,
            "cycle_time_hours": cycle_time,
            "review_count": pr.get("_review_count", 0),
            "reviewers": reviewers,
        })

    seed = int(hashlib.md5(team_name.encode()).hexdigest()[:8], 16)
    rng = random.Random(seed)

    for issue in transformed_issues:
        if issue["sprint_label"] and rng.random() < 0.15:
            sprint_name = issue["sprint_label"].replace("sprint:", "")
            for sprint in sprints:
                if sprint_name.endswith(f"26.{sprint['start_week']:02d}.{sprint['end_week']:02d}"):
                    s_start = datetime.fromisoformat(sprint["start_date"])
                    delay = timedelta(hours=rng.randint(1, 48))
                    new_created = (s_start + delay).isoformat()
                    issue["created_at"] = new_created
                    issue["created_after_sprint_start"] = True
                    break

    deploy_events = []
    for sprint in sprints:
        num_deploys = rng.randint(3, 7)
        s_start = datetime.fromisoformat(sprint["start_date"])
        s_end = datetime.fromisoformat(sprint["end_date"])
        span = (s_end - s_start).total_seconds()
        for _ in range(num_deploys):
            ts = s_start + timedelta(seconds=rng.random() * span)
            is_failure = rng.random() < 0.1
            deploy_events.append({
                "workflow_run_id": rng.randint(10**10, 10**11),
                "deployed_at": ts.isoformat(),
                "status": "failure" if is_failure else "success",
                "environment": rng.choice(["production", "production", "staging"]),
                "team": team_name,
                "sprint_name": sprint["name"],
            })

    incidents = []
    for sprint in sprints:
        num_incidents = rng.randint(0, 3)
        s_start = datetime.fromisoformat(sprint["start_date"])
        s_end = datetime.fromisoformat(sprint["end_date"])
        span = (s_end - s_start).total_seconds()
        team_deploys = [d for d in deploy_events if d["sprint_name"] == sprint["name"]]
        failed_deploys = [d for d in team_deploys if d["status"] == "failure"]
        for _ in range(num_incidents):
            created = s_start + timedelta(seconds=rng.random() * span)
            mttr = round(random.lognormvariate(0, 0.8), 2)
            mttr = max(0.5, min(mttr, 8))
            resolved = created + timedelta(hours=mttr)
            is_failure = rng.random() < 0.3 and failed_deploys
            linked = None
            if is_failure and failed_deploys:
                linked = rng.choice(failed_deploys)["workflow_run_id"]
            incidents.append({
                "pagerduty_id": f"inc_{team_name}_{sprint['name']}_{len(incidents)}",
                "title": rng.choice([
                    "High CPU alert on production", "Database connection pool exhausted",
                    "API latency spike", "Deployment failure rollback",
                    "Memory leak in worker pod", "SSL certificate expired",
                    "Queue backlog growing",
                ]),
                "status": "resolved",
                "created_at": created.isoformat(),
                "resolved_at": resolved.isoformat(),
                "mttr_hours": mttr,
                "is_change_failure": bool(is_failure),
                "linked_deploy_run_id": linked,
                "team": team_name,
                "sprint_name": sprint["name"],
            })

    sprints_out = []
    for sprint in sprints:
        sprints_out.append({
            "name": f"{team_name}-26.{sprint['start_week']:02d}.{sprint['end_week']:02d}",
            "start_date": sprint["start_date"],
            "end_date": sprint["end_date"],
            "team": team_name,
        })

    return {
        "team": team_name,
        "repo_full": repo_full,
        "engineers": list(eng_map.values()),
        "eng_map": eng_map,
        "sprints": sprints_out,
        "issues": transformed_issues,
        "pull_requests": transformed_pulls,
        "deploy_events": deploy_events,
        "incidents": incidents,
    }


def main():
    raw_dir = Path("data/raw")
    output_dir = Path("data/transformed")
    output_dir.mkdir(parents=True, exist_ok=True)

    if not raw_dir.exists():
        print("No data/raw/ directory found. Run tools/download_public_data.py first.")
        sys.exit(1)

    all_data = {}
    for repo_full, info in REPO_TEAM_MAP.items():
        result = process_repo(raw_dir, output_dir, repo_full, info)
        if result:
            all_data[info["team"]] = result

    combined = {
        "teams": list(all_data.keys()),
        "team_data": all_data,
    }
    out_path = output_dir / "sprintsense_test_data.json"
    with open(out_path, "w") as f:
        json.dump(combined, f, indent=2, default=str)

    total_issues = sum(len(td["issues"]) for td in all_data.values())
    total_prs = sum(len(td["pull_requests"]) for td in all_data.values())
    total_sprints = sum(len(td["sprints"]) for td in all_data.values())
    total_deploys = sum(len(td["deploy_events"]) for td in all_data.values())
    total_incidents = sum(len(td["incidents"]) for td in all_data.values())
    total_engineers = sum(len(td["engineers"]) for td in all_data.values())

    print(f"\n{'='*50}")
    print(f"Transformation complete!")
    print(f"  Teams: {len(all_data)}")
    print(f"  Engineers: {total_engineers}")
    print(f"  Sprints: {total_sprints}")
    print(f"  Issues: {total_issues}")
    print(f"  PRs: {total_prs}")
    print(f"  Deploy events: {total_deploys}")
    print(f"  Incidents: {total_incidents}")
    print(f"  Output: {out_path}")


import sys

if __name__ == "__main__":
    main()
