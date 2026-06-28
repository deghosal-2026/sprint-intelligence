"""Phase 1: Fetch data from GitHub API and store in DB."""

from datetime import datetime, timezone
from api.models import Repo, Issue, PullRequest, DeployEvent, db
from . import config as cfg
from . import github_client as gh


def compute_cycle_time(first_commit_at, merged_at):
    if not first_commit_at or not merged_at:
        return None
    try:
        fc = datetime.fromisoformat(first_commit_at.replace("Z", "+00:00"))
        mg = datetime.fromisoformat(merged_at.replace("Z", "+00:00"))
        return round((mg - fc).total_seconds() / 3600, 2)
    except (ValueError, TypeError):
        return None


def parse_labels(raw_labels, label_cfg):
    points = None
    is_bug = False
    is_feature = False
    is_techdebt = False
    is_task = False
    is_blocked = False
    sprint_label = None

    for label in raw_labels:
        name = label.get("name", "")
        if name.startswith(label_cfg.points_prefix):
            try:
                points = float(name.split(":")[1])
            except (ValueError, IndexError):
                pass
        elif name == label_cfg.bug_label:
            is_bug = True
        elif name == label_cfg.feature_label:
            is_feature = True
        elif name == label_cfg.techdebt_label:
            is_techdebt = True
        elif name == label_cfg.task_label:
            is_task = True
        elif name == "blocked":
            is_blocked = True
        elif name.startswith(label_cfg.sprint_prefix):
            sprint_label = name

    return points, is_bug, is_feature, is_techdebt, is_task, is_blocked, sprint_label


def fetch_six_months_ago():
    now = datetime.now(timezone.utc)
    try:
        return now.replace(month=now.month - 6)
    except ValueError:
        return now.replace(year=now.year - 1, month=now.month + 6)


def run_fetch():
    cfg.sync_config()
    repos = Repo.query.all()
    since = fetch_six_months_ago()

    results = {}
    for repo in repos:
        owner, name = repo.owner, repo.name
        print(f"  Fetching {owner}/{name}...")
        label_cfg = repo.label_config
        repo_results = {"issues": 0, "prs": 0, "milestones": 0, "deploys": 0, "errors": []}

        try:
            raw_issues = gh.fetch_issues(owner, name, since)
            for item in raw_issues:
                if "pull_request" in item:
                    continue
                points, is_bug, is_feature, is_techdebt, is_task, is_blocked, sprint_label = \
                    parse_labels(item.get("labels", []), label_cfg)
                assignee = item.get("assignee", {}) or {}
                milestone = item.get("milestone")

                issue = Issue(
                    github_id=item["id"],
                    repo_id=repo.id,
                    number=item["number"],
                    title=item.get("title"),
                    state=item.get("state"),
                    created_at=item.get("created_at"),
                    closed_at=item.get("closed_at"),
                    updated_at=item.get("updated_at"),
                    assignee_login=assignee.get("login") if assignee else None,
                    story_points=points,
                    is_bug=is_bug,
                    is_feature=is_feature,
                    is_techdebt=is_techdebt,
                    is_task=is_task,
                    is_blocked=is_blocked,
                    milestone_title=milestone.get("title") if milestone else None,
                    raw_json=item,
                )
                db.session.merge(issue)
                repo_results["issues"] += 1

            raw_pulls = gh.fetch_pulls(owner, name)
            for pr in raw_pulls:
                pr_num = pr["number"]
                first_commit = gh.fetch_first_commit(owner, name, pr_num)
                review_count, reviewers = gh.fetch_reviews(owner, name, pr_num)
                cycle_time = compute_cycle_time(first_commit, pr.get("merged_at"))

                author = pr.get("user", {}) or {}
                pr_record = PullRequest(
                    github_id=pr["id"],
                    repo_id=repo.id,
                    number=pr_num,
                    title=pr.get("title"),
                    state="merged" if pr.get("merged_at") else pr.get("state"),
                    author_login=author.get("login"),
                    created_at=pr.get("created_at"),
                    merged_at=pr.get("merged_at"),
                    closed_at=pr.get("closed_at"),
                    first_commit_at=first_commit,
                    cycle_time_hours=cycle_time,
                    review_count=review_count,
                    reviewers=reviewers,
                    raw_json=pr,
                )
                db.session.merge(pr_record)
                repo_results["prs"] += 1

            milestones = gh.fetch_milestones(owner, name)
            repo_results["milestones"] = len(milestones)

            workflow_runs = gh.fetch_workflow_runs(owner, name)
            for run in workflow_runs:
                run_name = (run.get("name") or "").lower()
                if any(kw in run_name for kw in ["deploy", "release", "production"]):
                    deploy = DeployEvent(
                        repo_id=repo.id,
                        workflow_run_id=run["id"],
                        deployed_at=run.get("created_at") or run.get("updated_at"),
                        status=run.get("conclusion", "unknown"),
                        environment="production" if "production" in run_name else "staging",
                    )
                    db.session.merge(deploy)
                    repo_results["deploys"] += 1

            db.session.commit()
            print(f"    {repo_results['issues']} issues, {repo_results['prs']} PRs")

        except Exception as e:
            db.session.rollback()
            repo_results["errors"].append(str(e))
            print(f"    ERROR: {e}")

        results[f"{owner}/{name}"] = repo_results

    return results
