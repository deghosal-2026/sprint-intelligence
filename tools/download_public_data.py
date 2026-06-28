"""Download issues, PRs, and milestones from 10 public repos via GitHub API.

Runs in 3 time-window batches (0-30d, 30-60d, 60-90d).
Saves 100-entry chunks per type per repo.
Resumes: skips batches that already have chunk files on disk.
"""

import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

REPOS = [
    "microsoft/vscode",
    "facebook/react",
    "nodejs/node",
    "kubernetes/kubernetes",
    "rust-lang/rust",
    "vercel/next.js",
    "grafana/grafana",
    "angular/angular",
    "python/cpython",
    "tensorflow/tensorflow",
]

MAX_PER_REPO = 500
CHUNK_SIZE = 100
PER_PAGE = 100
MAX_API_PAGES = 10

BASE_URL = "https://api.github.com"
TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Accept": "application/vnd.github.v3+json"}
if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"

OUTPUT_DIR = Path("data/raw")
BATCH_WINDOWS = [
    ("A_last30d", 0, 30),
    ("B_30to60d", 30, 60),
    ("C_60to90d", 60, 90),
]


def stamp():
    return datetime.now().strftime("%H:%M:%S")


def log(msg):
    print(f"[{stamp()}] {msg}", flush=True)


def days_ago(d):
    now = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    return now - timedelta(days=d)


def rate_limit_sleep(response):
    remaining = int(response.headers.get("X-RateLimit-Remaining", 100))
    if remaining < 50:
        reset_ts = int(response.headers.get("X-RateLimit-Reset", time.time() + 60))
        s = max(reset_ts - time.time() + 1, 0)
        log(f"  Rate limit low ({remaining}). Sleep {s:.0f}s...")
        time.sleep(s)
    return remaining


def fetch_paginated(url, params=None, max_pages=MAX_API_PAGES):
    if params is None:
        params = {}
    params["per_page"] = PER_PAGE
    all_items = []
    page = 1
    while page <= max_pages:
        params["page"] = page
        resp = requests.get(url, headers=HEADERS, params=params, timeout=60)
        rate_limit_sleep(resp)
        if resp.status_code == 403 and "rate limit" in resp.text.lower():
            reset_ts = int(resp.headers.get("X-RateLimit-Reset", time.time() + 60))
            s = max(reset_ts - time.time() + 1, 0)
            log(f"  Rate limited! Sleep {s:.0f}s...")
            time.sleep(s)
            continue
        if resp.status_code == 404:
            log(f"  404: {url}")
            return []
        resp.raise_for_status()
        data = resp.json()
        if not data:
            break
        all_items.extend(data)
        if len(data) < PER_PAGE:
            break
        page += 1
    return all_items


def fetch_issues(owner, repo, since_date, until_date):
    """Fetch issues updated in [since_date, until_date)."""
    url = f"{BASE_URL}/repos/{owner}/{repo}/issues"
    since_str = since_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    items = fetch_paginated(url, {"state": "all", "since": since_str, "filter": "all"})
    filtered = [
        i for i in items
        if i.get("updated_at") and until_date
        and i["updated_at"] < until_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    ]
    return filtered[:MAX_PER_REPO]


def fetch_pulls(owner, repo, since_date, until_date):
    """Fetch PRs updated in [since_date, until_date)."""
    url = f"{BASE_URL}/repos/{owner}/{repo}/pulls"
    since_str = since_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    items = fetch_paginated(url, {
        "state": "all", "sort": "updated", "direction": "desc", "since": since_str,
    })
    filtered = [
        p for p in items
        if p.get("updated_at") and until_date
        and p["updated_at"] < until_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    ]
    return filtered[:MAX_PER_REPO]


def save_chunks(items, dir_path, prefix):
    """Split `items` into CHUNK_SIZE batches, save as prefix_001.json etc."""
    saved = 0
    for ci in range(0, len(items), CHUNK_SIZE):
        chunk = items[ci : ci + CHUNK_SIZE]
        chunk_file = dir_path / f"{prefix}_{ci // CHUNK_SIZE + 1:03d}.json"
        with open(chunk_file, "w") as f:
            json.dump(chunk, f, default=str)
        saved += len(chunk)
    return saved


def load_chunks(dir_path, prefix):
    """Load all saved chunks for a prefix, return combined list."""
    items = []
    idx = 1
    while True:
        chunk_file = dir_path / f"{prefix}_{idx:03d}.json"
        if not chunk_file.exists():
            break
        with open(chunk_file) as f:
            items.extend(json.load(f))
        idx += 1
    return items


def batch_already_done(dir_path, prefix):
    """Check if any chunk files already exist for this batch."""
    return any(dir_path.glob(f"{prefix}_*.json"))


def run_all():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if not TOKEN:
        log("WARNING: GITHUB_TOKEN not set. Rate limit = 60/hr.")

    total_repos = len(REPOS)
    for ri, repo_full in enumerate(REPOS, 1):
        owner, repo_name = repo_full.split("/")
        repo_dir = OUTPUT_DIR / f"{owner}_{repo_name}"
        repo_dir.mkdir(parents=True, exist_ok=True)

        log(f"=== Repo {ri}/{total_repos}: {owner}/{repo_name} ===")

        for batch_id, since_days, until_days in BATCH_WINDOWS:
            since_date = days_ago(until_days)
            until_date = days_ago(since_days) if since_days > 0 else datetime.now(timezone.utc)

            log(f"  Batch {batch_id}: {since_date.date()} → {until_date.date()}")

            # Issues
            issues_prefix = f"issues_{batch_id}"
            if batch_already_done(repo_dir, issues_prefix):
                loaded = load_chunks(repo_dir, issues_prefix)
                log(f"    issues: SKIP (already {len(loaded)} entries)")
            else:
                log(f"    Fetching issues...")
                try:
                    issues = fetch_issues(owner, repo_name, since_date, until_date)
                    n = save_chunks(issues, repo_dir, issues_prefix)
                    log(f"    issues: {n} entries saved")
                except Exception as e:
                    log(f"    issues: FAILED {e}")

            # PRs
            pulls_prefix = f"pulls_{batch_id}"
            if batch_already_done(repo_dir, pulls_prefix):
                loaded = load_chunks(repo_dir, pulls_prefix)
                log(f"    pulls:  SKIP (already {len(loaded)} entries)")
            else:
                log(f"    Fetching PRs...")
                try:
                    pulls = fetch_pulls(owner, repo_name, since_date, until_date)
                    n = save_chunks(pulls, repo_dir, pulls_prefix)
                    log(f"    pulls:  {n} entries saved")
                except Exception as e:
                    log(f"    pulls: FAILED {e}")

            time.sleep(1)

        # Milestones
        milestones_file = repo_dir / "milestones.json"
        if milestones_file.exists():
            log(f"  milestones: SKIP (already exists)")
        else:
            log(f"  Fetching milestones...")
            try:
                milestones = fetch_paginated(
                    f"{BASE_URL}/repos/{owner}/{repo_name}/milestones",
                    {"state": "all"},
                )
                with open(milestones_file, "w") as f:
                    json.dump(milestones, f, default=str)
                log(f"  milestones: {len(milestones)} saved")
            except Exception as e:
                log(f"  milestones: FAILED {e}")

        log(f"  ✓ done with {owner}/{repo_name}")
        time.sleep(1)

    log(f"\nALL DONE. Files in {OUTPUT_DIR.resolve()}/")


def run_test():
    """Quick test: 1 repo, last 2 weeks. 5 min timeout."""
    import signal

    def timeout_handler(signum, frame):
        log("TIMEOUT (5 min)")
        sys.exit(1)

    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(300)

    test_repo = sys.argv[2] if len(sys.argv) > 2 else "facebook/react"
    owner, repo_name = test_repo.split("/")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    repo_dir = OUTPUT_DIR / f"{owner}_{repo_name}"
    repo_dir.mkdir(parents=True, exist_ok=True)

    since_date = days_ago(14)
    until_date = datetime.now(timezone.utc)
    log(f"TEST: {test_repo}, 2 weeks ({since_date.date()} → {until_date.date()})")

    log("  Fetching issues...")
    issues = fetch_issues(owner, repo_name, since_date, until_date)
    n = save_chunks(issues, repo_dir, "issues_001")
    log(f"  issues: {n} entries saved")

    log("  Fetching PRs...")
    pulls = fetch_pulls(owner, repo_name, since_date, until_date)
    n = save_chunks(pulls, repo_dir, "pulls_001")
    log(f"  pulls: {n} entries saved")

    log("  Fetching milestones...")
    milestones = fetch_paginated(
        f"{BASE_URL}/repos/{owner}/{repo_name}/milestones", {"state": "all"},
    )
    with open(repo_dir / "milestones.json", "w") as f:
        json.dump(milestones, f, default=str)
    log(f"  milestones: {len(milestones)} saved")

    log("TEST DONE.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_test()
    else:
        run_all()
