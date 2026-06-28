"""Download issues, PRs, and milestones from 10 public repos via GitHub API."""

import json
import os
import sys
import time
from datetime import datetime, timezone
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

SIX_MONTHS_AGO = datetime.now(timezone.utc).replace(
    hour=0, minute=0, second=0, microsecond=0
)
try:
    SIX_MONTHS_AGO = SIX_MONTHS_AGO.replace(month=SIX_MONTHS_AGO.month - 6)
except ValueError:
    SIX_MONTHS_AGO = SIX_MONTHS_AGO.replace(
        year=SIX_MONTHS_AGO.year - 1, month=SIX_MONTHS_AGO.month + 6
    )

BASE_URL = "https://api.github.com"
TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Accept": "application/vnd.github.v3+json"}
if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"


def rate_limit_sleep(response):
    remaining = int(response.headers.get("X-RateLimit-Remaining", 100))
    if remaining < 50:
        reset_ts = int(response.headers.get("X-RateLimit-Reset", time.time() + 60))
        sleep_time = max(reset_ts - time.time() + 1, 0)
        print(f"  Rate limit low ({remaining}). Sleeping {sleep_time:.0f}s...")
        time.sleep(sleep_time)


def fetch_paginated(url, params=None):
    if params is None:
        params = {}
    params["per_page"] = 100
    all_items = []
    page = 1
    while True:
        params["page"] = page
        resp = requests.get(url, headers=HEADERS, params=params, timeout=30)
        rate_limit_sleep(resp)
        if resp.status_code == 403 and "rate limit" in resp.text.lower():
            reset_ts = int(resp.headers.get("X-RateLimit-Reset", time.time() + 60))
            sleep_time = max(reset_ts - time.time() + 1, 0)
            print(f"  Rate limited. Sleeping {sleep_time:.0f}s...")
            time.sleep(sleep_time)
            continue
        if resp.status_code == 404:
            print(f"  Not found (404): {url}")
            return []
        resp.raise_for_status()
        data = resp.json()
        if not data:
            break
        all_items.extend(data)
        if len(data) < 100:
            break
        page += 1
    return all_items


def download_issues(owner, repo, output_dir):
    print(f"  Fetching issues...")
    url = f"{BASE_URL}/repos/{owner}/{repo}/issues"
    since_str = SIX_MONTHS_AGO.strftime("%Y-%m-%dT%H:%M:%SZ")
    issues = fetch_paginated(url, {"state": "all", "since": since_str, "filter": "all"})
    out_path = output_dir / f"{owner}_{repo}_issues.json"
    with open(out_path, "w") as f:
        json.dump(issues, f, default=str)
    print(f"    {len(issues)} issues saved to {out_path.name}")
    return out_path


def download_pulls(owner, repo, output_dir):
    print(f"  Fetching PRs...")
    url = f"{BASE_URL}/repos/{owner}/{repo}/pulls"
    pulls = fetch_paginated(url, {"state": "all", "sort": "updated", "direction": "desc"})

    for pr in pulls:
        pr_num = pr["number"]
        commit_url = f"{BASE_URL}/repos/{owner}/{repo}/pulls/{pr_num}/commits"
        try:
            cresp = requests.get(commit_url, headers=HEADERS, params={"per_page": 1}, timeout=15)
            if cresp.status_code == 200 and cresp.json():
                first_commit = cresp.json()[0]["commit"]["author"]["date"]
                pr["_first_commit_at"] = first_commit
            rate_limit_sleep(cresp)
        except Exception:
            pr["_first_commit_at"] = None

        review_url = f"{BASE_URL}/repos/{owner}/{repo}/pulls/{pr_num}/reviews"
        try:
            rresp = requests.get(review_url, headers=HEADERS, params={"per_page": 100}, timeout=15)
            if rresp.status_code == 200:
                reviews = rresp.json()
                pr["_review_count"] = len(reviews)
                pr["_reviewers"] = list(set(
                    r["user"]["login"] for r in reviews if r.get("user")
                ))
            rate_limit_sleep(rresp)
        except Exception:
            pr["_review_count"] = 0
            pr["_reviewers"] = []

    out_path = output_dir / f"{owner}_{repo}_pulls.json"
    with open(out_path, "w") as f:
        json.dump(pulls, f, default=str)
    print(f"    {len(pulls)} PRs saved to {out_path.name}")
    return out_path


def download_milestones(owner, repo, output_dir):
    print(f"  Fetching milestones...")
    url = f"{BASE_URL}/repos/{owner}/{repo}/milestones"
    milestones = fetch_paginated(url, {"state": "all"})
    out_path = output_dir / f"{owner}_{repo}_milestones.json"
    with open(out_path, "w") as f:
        json.dump(milestones, f, default=str)
    print(f"    {len(milestones)} milestones saved to {out_path.name}")
    return out_path


def main():
    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)

    if not TOKEN:
        print("WARNING: GITHUB_TOKEN not set. API requests will be heavily rate limited.")

    for repo_full in REPOS:
        owner, repo = repo_full.split("/")
        print(f"\n=== {owner}/{repo} ===")
        try:
            download_issues(owner, repo, output_dir)
            download_pulls(owner, repo, output_dir)
            download_milestones(owner, repo, output_dir)
        except Exception as e:
            print(f"  FAILED: {e}")

    print("\nDone. Raw data in data/raw/")


if __name__ == "__main__":
    main()
