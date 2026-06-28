"""Sync sprintsense-config.json from GitHub into DB config tables."""

import json
import os
from pathlib import Path
import requests

from api.models import Repo, LabelConfig, Threshold, db

CONFIG_URL = os.getenv(
    "CONFIG_URL",
    "https://raw.githubusercontent.com/deghosal-2026/sprint-intelligence/main/sprintsense-config.json",
)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def fetch_config():
    headers = {"Accept": "application/vnd.github.v3.raw"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    try:
        resp = requests.get(CONFIG_URL, headers=headers, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        here = Path(__file__).resolve().parent.parent.parent / "sprintsense-config.json"
        if here.exists():
            with open(here) as f:
                return json.load(f)
        raise


def sync_config(config=None):
    if config is None:
        config = fetch_config()

    results = {"repos": 0, "labels": 0, "thresholds": 0}

    for repo_entry in config.get("repos", []):
        existing = Repo.query.filter_by(
            owner=repo_entry["owner"], name=repo_entry["name"]
        ).first()
        if existing:
            existing.team = repo_entry.get("team")
        else:
            repo = Repo(
                owner=repo_entry["owner"],
                name=repo_entry["name"],
                team=repo_entry.get("team"),
            )
            db.session.add(repo)
        results["repos"] += 1

    db.session.flush()

    labels_config = config.get("labels", {})
    for repo in Repo.query.all():
        existing = LabelConfig.query.filter_by(repo_id=repo.id).first()
        if existing:
            existing.points_prefix = labels_config.get("points_prefix", "points:")
            existing.bug_label = labels_config.get("bug", "bug")
            existing.feature_label = labels_config.get("feature", "feature")
            existing.techdebt_label = labels_config.get("tech_debt", "tech-debt")
            existing.task_label = labels_config.get("task", "task")
            existing.sprint_prefix = labels_config.get("sprint_prefix", "sprint:")
        else:
            lc = LabelConfig(
                repo_id=repo.id,
                points_prefix=labels_config.get("points_prefix", "points:"),
                bug_label=labels_config.get("bug", "bug"),
                feature_label=labels_config.get("feature", "feature"),
                techdebt_label=labels_config.get("tech_debt", "tech-debt"),
                task_label=labels_config.get("task", "task"),
                sprint_prefix=labels_config.get("sprint_prefix", "sprint:"),
            )
            db.session.add(lc)
        results["labels"] += 1

    thresholds_config = config.get("thresholds", {})
    for key, value in thresholds_config.items():
        existing = Threshold.query.filter_by(key=key).first()
        if existing:
            existing.value = str(value)
        else:
            t = Threshold(key=key, value=str(value))
            db.session.add(t)
        results["thresholds"] += 1

    db.session.commit()
    return results
