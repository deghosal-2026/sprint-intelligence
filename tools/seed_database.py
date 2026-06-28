"""Load transformed test data into PostgreSQL, then run Phase 2 compute."""

import json
import os
import sys
from pathlib import Path

import psycopg2

TRANSFORMED_PATH = Path("data/transformed/sprintsense_test_data.json")
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://sprintsense:devpassword123@localhost:5432/sprintsense",
)


def get_conn():
    return psycopg2.connect(DATABASE_URL)


def seed_repos(conn, team_data):
    cur = conn.cursor()
    repo_map = {}
    for team_name, td in team_data.items():
        owner, repo_name = td["repo_full"].split("/")
        cur.execute(
            "INSERT INTO repos (owner, name, team) VALUES (%s, %s, %s) "
            "ON CONFLICT (owner, name) DO UPDATE SET team = EXCLUDED.team RETURNING id",
            (owner, repo_name, team_name),
        )
        repo_id = cur.fetchone()[0]
        repo_map[team_name] = repo_id
        print(f"  Repo {owner}/{repo_name} → id={repo_id} (team={team_name})")
    conn.commit()
    return repo_map


def seed_label_config(conn, repo_map):
    cur = conn.cursor()
    for team_name, repo_id in repo_map.items():
        cur.execute(
            "INSERT INTO label_config (repo_id) VALUES (%s) ON CONFLICT (repo_id) DO NOTHING",
            (repo_id,),
        )
    conn.commit()
    print(f"  Label config seeded for {len(repo_map)} repos")


def seed_sprints(conn, team_data, repo_map):
    cur = conn.cursor()
    sprint_map = {}
    for team_name, td in team_data.items():
        repo_id = repo_map[team_name]
        for sprint in td["sprints"]:
            cur.execute(
                "INSERT INTO sprints (name, start_date, end_date, source_type, source_id, repo_id) "
                "VALUES (%s, %s::date, %s::date, 'synthetic', 'test_data', %s) "
                "ON CONFLICT (name) DO UPDATE SET repo_id = EXCLUDED.repo_id RETURNING id",
                (sprint["name"], sprint["start_date"][:10], sprint["end_date"][:10], repo_id),
            )
            sprint_id = cur.fetchone()[0]
            sprint_map[sprint["name"]] = sprint_id
    conn.commit()
    print(f"  {len(sprint_map)} sprints seeded")
    return sprint_map


def seed_issues(conn, team_data, repo_map, sprint_map):
    cur = conn.cursor()
    issue_id_map = {}
    total = 0
    for team_name, td in team_data.items():
        repo_id = repo_map[team_name]
        for issue in td["issues"]:
            cur.execute(
                """INSERT INTO issues
                   (github_id, repo_id, number, title, state, created_at, closed_at,
                    updated_at, assignee_login, story_points, is_bug, is_feature,
                    is_techdebt, is_task, is_blocked, milestone_title)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                   ON CONFLICT (github_id, repo_id) DO UPDATE SET title = EXCLUDED.title
                   RETURNING id""",
                (
                    issue["github_id"], repo_id, issue["number"], issue["title"],
                    issue["state"], issue["created_at"], issue["closed_at"],
                    issue["updated_at"], issue["assignee_login"],
                    issue["story_points"], issue["is_bug"], issue["is_feature"],
                    issue["is_techdebt"], issue["is_task"], issue["is_blocked"],
                    issue["milestone_title"],
                ),
            )
            issue_db_id = cur.fetchone()[0]
            issue_id_map[issue["github_id"]] = issue_db_id
            total += 1

            if issue["sprint_label"]:
                sprint_name = issue["sprint_label"].replace("sprint:", "")
                if sprint_name in sprint_map:
                    cur.execute(
                        "INSERT INTO issue_sprint_map (issue_id, sprint_id) "
                        "VALUES (%s, %s) ON CONFLICT DO NOTHING",
                        (issue_db_id, sprint_map[sprint_name]),
                    )
    conn.commit()
    print(f"  {total} issues + sprint mappings seeded")
    return issue_id_map


def seed_pull_requests(conn, team_data, repo_map):
    cur = conn.cursor()
    pr_id_map = {}
    total = 0
    for team_name, td in team_data.items():
        repo_id = repo_map[team_name]
        for pr in td["pull_requests"]:
            reviewers_list = pr.get("reviewers") or []
            cur.execute(
                """INSERT INTO pull_requests
                   (github_id, repo_id, number, title, state, author_login,
                    created_at, merged_at, closed_at, first_commit_at,
                    cycle_time_hours, review_count, reviewers)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                   ON CONFLICT (github_id, repo_id) DO UPDATE SET title = EXCLUDED.title
                   RETURNING id""",
                (
                    pr["github_id"], repo_id, pr["number"], pr["title"],
                    pr["state"], pr["author_login"], pr["created_at"],
                    pr["merged_at"], pr["closed_at"], pr["first_commit_at"],
                    pr["cycle_time_hours"], pr["review_count"], reviewers_list,
                ),
            )
            pr_id = cur.fetchone()[0]
            pr_id_map[pr["github_id"]] = pr_id
            total += 1
    conn.commit()
    print(f"  {total} PRs seeded")
    return pr_id_map


def seed_deploy_events(conn, team_data, repo_map, sprint_map):
    cur = conn.cursor()
    deploy_id_map = {}
    total = 0
    for team_name, td in team_data.items():
        repo_id = repo_map[team_name]
        for deploy in td["deploy_events"]:
            cur.execute(
                "INSERT INTO deploy_events (repo_id, workflow_run_id, deployed_at, status, environment) "
                "VALUES (%s, %s, %s, %s, %s) ON CONFLICT (workflow_run_id, repo_id) DO NOTHING RETURNING id",
                (repo_id, deploy["workflow_run_id"], deploy["deployed_at"],
                 deploy["status"], deploy["environment"]),
            )
            row = cur.fetchone()
            if row:
                deploy_id_map[deploy["workflow_run_id"]] = row[0]
                total += 1
    conn.commit()
    print(f"  {total} deploy events seeded")
    return deploy_id_map


def seed_incidents(conn, team_data, deploy_id_map):
    cur = conn.cursor()
    total = 0
    for team_name, td in team_data.items():
        for inc in td["incidents"]:
            linked_deploy_id = None
            if inc["linked_deploy_run_id"] and inc["linked_deploy_run_id"] in deploy_id_map:
                linked_deploy_id = deploy_id_map[inc["linked_deploy_run_id"]]
            cur.execute(
                "INSERT INTO incidents (pagerduty_id, title, status, created_at, resolved_at, mttr_hours, is_change_failure, linked_deploy_id) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (pagerduty_id) DO NOTHING",
                (inc["pagerduty_id"], inc["title"], inc["status"],
                 inc["created_at"], inc["resolved_at"], inc["mttr_hours"],
                 inc["is_change_failure"], linked_deploy_id),
            )
            total += 1
    conn.commit()
    print(f"  {total} incidents seeded")


def seed_thresholds(conn):
    cur = conn.cursor()
    defaults = [
        ("stale_pr_days", "3"),
        ("max_wip", "4"),
        ("scope_creep_points", "6"),
    ]
    for key, value in defaults:
        cur.execute(
            "INSERT INTO thresholds (key, value) VALUES (%s, %s) ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value",
            (key, value),
        )
    conn.commit()
    print("  Thresholds seeded")


def main():
    if not TRANSFORMED_PATH.exists():
        print(f"Error: {TRANSFORMED_PATH} not found. Run tools/transform_test_data.py first.")
        sys.exit(1)

    with open(TRANSFORMED_PATH) as f:
        data = json.load(f)

    team_data = data["team_data"]
    print(f"Seeding data for {len(team_data)} teams...")

    conn = get_conn()
    try:
        print("\n1. Seeding repos...")
        repo_map = seed_repos(conn, team_data)

        print("\n2. Seeding label config...")
        seed_label_config(conn, repo_map)

        print("\n3. Seeding sprints...")
        sprint_map = seed_sprints(conn, team_data, repo_map)

        print("\n4. Seeding issues + sprint mappings...")
        seed_issues(conn, team_data, repo_map, sprint_map)

        print("\n5. Seeding pull requests...")
        seed_pull_requests(conn, team_data, repo_map)

        print("\n6. Seeding deploy events...")
        deploy_id_map = seed_deploy_events(conn, team_data, repo_map, sprint_map)

        print("\n7. Seeding incidents...")
        seed_incidents(conn, team_data, deploy_id_map)

        print("\n8. Seeding thresholds...")
        seed_thresholds(conn)

        print(f"\n{'='*50}")
        print("Database seeded successfully!")
        print("Run `python -m poller --compute` to compute metrics.")

    finally:
        conn.close()


if __name__ == "__main__":
    main()
