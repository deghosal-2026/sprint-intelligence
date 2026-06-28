"""GitHub REST API wrapper with pagination and rate-limit handling."""

import os
import time
from datetime import datetime, timezone

import requests

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
    return remaining


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
            print(f"  Not found: {url}")
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


def get_rate_limit_remaining():
    try:
        resp = requests.get(f"{BASE_URL}/rate_limit", headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            return resp.json().get("resources", {}).get("core", {}).get("remaining", 0)
    except Exception:
        pass
    return 0


def fetch_issues(owner, repo, since=None):
    url = f"{BASE_URL}/repos/{owner}/{repo}/issues"
    params = {"state": "all", "filter": "all"}
    if since:
        params["since"] = since.strftime("%Y-%m-%dT%H:%M:%SZ") if hasattr(since, "strftime") else since
    return fetch_paginated(url, params)


def fetch_pulls(owner, repo):
    url = f"{BASE_URL}/repos/{owner}/{repo}/pulls"
    return fetch_paginated(url, {"state": "all", "sort": "updated", "direction": "desc"})


def fetch_first_commit(owner, repo, pr_number):
    url = f"{BASE_URL}/repos/{owner}/{repo}/pulls/{pr_number}/commits"
    try:
        resp = requests.get(url, headers=HEADERS, params={"per_page": 1}, timeout=15)
        rate_limit_sleep(resp)
        if resp.status_code == 200 and resp.json():
            return resp.json()[0]["commit"]["author"]["date"]
    except Exception:
        pass
    return None


def fetch_reviews(owner, repo, pr_number):
    url = f"{BASE_URL}/repos/{owner}/{repo}/pulls/{pr_number}/reviews"
    try:
        resp = requests.get(url, headers=HEADERS, params={"per_page": 100}, timeout=15)
        rate_limit_sleep(resp)
        if resp.status_code == 200:
            reviews = resp.json()
            reviewers = list(set(r["user"]["login"] for r in reviews if r.get("user")))
            return len(reviews), reviewers
    except Exception:
        pass
    return 0, []


def fetch_milestones(owner, repo):
    url = f"{BASE_URL}/repos/{owner}/{repo}/milestones"
    return fetch_paginated(url, {"state": "all"})


def fetch_workflow_runs(owner, repo, since=None):
    url = f"{BASE_URL}/repos/{owner}/{repo}/actions/runs"
    params = {"status": "completed"}
    if since:
        params["created"] = f">={since.strftime('%Y-%m-%d') if hasattr(since, 'strftime') else since}"
    return fetch_paginated(url, params)
