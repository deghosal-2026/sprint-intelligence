"""Anonymize raw GitHub data, fabricate sprint structure, generate synthetic events."""

import hashlib
import json
import math
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


def load_chunked(repo_dir, prefix):
    """Load all chunked JSON files matching prefix_*.json, deduplicate by 'id'."""
    items = []
    seen = set()
    for path in sorted(repo_dir.glob(f"{prefix}_*.json")):
        with open(path) as f:
            chunk = json.load(f)
        for item in chunk:
            iid = item.get("id")
            if iid not in seen:
                items.append(item)
                seen.add(iid)
    return items


def process_repo(raw_dir, output_dir, repo_full, team_info):
    owner, repo_name = repo_full.split("/")
    team_name = team_info["team"]
    eng_count = team_info["engineers"]
    print(f"  Processing {repo_full} → {team_name}")

    repo_dir = raw_dir / f"{owner}_{repo_name}"
    if not repo_dir.exists() or not repo_dir.is_dir():
        print(f"    No data directory found, skipping")
        return None

    raw_issues = load_chunked(repo_dir, "issues")
    raw_pulls = load_chunked(repo_dir, "pulls")

    if not raw_issues:
        print(f"    No issue files found, skipping")
        return None

    raw_milestones = []
    ms_file = repo_dir / "milestones.json"
    if ms_file.exists():
        with open(ms_file) as f:
            raw_milestones = json.load(f)

    print(f"    Loaded {len(raw_issues)} issues, {len(raw_pulls)} PRs, {len(raw_milestones)} milestones")

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
        return orig

    def assign_sprint(items, sprint_key):
        sorted_items = sorted(items, key=lambda x: x.get(sprint_key, "") or "")
        items_per = max(1, math.ceil(len(sorted_items) / len(sprints)))
        for idx, item in enumerate(sorted_items):
            sprint = sprints[min(idx // items_per, len(sprints) - 1)]
            yield item, sprint

    def map_to_engineer(login):
        if login in eng_map:
            return eng_map[login]
        return f"{team_name}-external-{hashlib.md5(login.encode()).hexdigest()[:6]}"

    transformed_issues = []
    for issue, sprint in assign_sprint(raw_issues, "created_at"):
        gh_id = issue["id"]
        issue_type, points = assign_properties(gh_id)
        created_dt = shift_date(issue.get("created_at"))
        closed_dt = shift_date(issue.get("closed_at"))
        assignee = issue.get("assignee")
        assignee_login = map_to_engineer(assignee["login"]) if assignee and assignee.get("login") else None

        sprint_label = f"sprint:{team_name}-{sprint['name']}"

        labels = issue.get("labels", [])
        label_names = [l.get("name", "") for l in labels] if labels else []
        is_blocked = "blocked" in label_names

        transformed_issues.append({
            "github_id": gh_id,
            "number": issue["number"],
            "title": issue.get("title", ""),
            "state": issue.get("state", "open"),
            "created_at": created_dt.isoformat() if created_dt else None,
            "closed_at": closed_dt.isoformat() if closed_dt else None,
            "updated_at": created_dt.isoformat() if created_dt else None,
            "assignee_login": assignee_login,
            "story_points": points,
            "is_bug": issue_type == "bug",
            "is_feature": issue_type == "feature",
            "is_techdebt": issue_type == "tech-debt",
            "is_task": issue_type == "task",
            "milestone_title": None,
            "sprint_label": sprint_label,
            "labels": label_names,
            "is_blocked": is_blocked,
        })

    transformed_pulls = []
    for pr in raw_pulls:
        gh_id = pr["id"]
        created = shift_date(pr.get("created_at"))
        merged = shift_date(pr.get("merged_at"))
        closed = shift_date(pr.get("closed_at"))

        first_commit_dt = shift_date(pr.get("_first_commit_at"))
        cycle_time = None
        if first_commit_dt and merged and merged.tzinfo is None and first_commit_dt.tzinfo is None:
            cycle_time = round((merged - first_commit_dt).total_seconds() / 3600, 2)

        author = pr.get("user", {})
        author_login = map_to_engineer(author.get("login")) if author else None

        raw_reviewers = pr.get("_reviewers", []) or []
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
            "first_commit_at": first_commit_dt.isoformat() if first_commit_dt else None,
            "cycle_time_hours": cycle_time,
            "review_count": pr.get("_review_count", 0) or 0,
            "reviewers": reviewers,
        })

    seed = int(hashlib.md5(team_name.encode()).hexdigest()[:8], 16)
    rng = random.Random(seed)

    for issue in transformed_issues:
        if issue["sprint_label"] and rng.random() < 0.15:
            sprint_name = issue["sprint_label"].replace("sprint:", "")
            for sprint in sprints:
                if sprint_name.endswith(sprint['name']):
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
            "name": f"{team_name}-{sprint['name']}",
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
