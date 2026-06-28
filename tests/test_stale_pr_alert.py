"""Stale PR alert — PRs older than threshold trigger alert."""

from datetime import datetime, timedelta


def is_stale(pr_created_at, threshold_days, pr_state="open", now=None):
    if pr_state != "open":
        return False
    if now is None:
        now = datetime.utcnow()
    return pr_created_at < (now - timedelta(days=threshold_days))


def test_pr_older_than_threshold_is_stale():
    now = datetime(2026, 6, 28, 12, 0, 0)
    created = now - timedelta(days=5)
    assert is_stale(created, threshold_days=3, now=now) is True


def test_pr_newer_than_threshold_not_stale():
    now = datetime(2026, 6, 28, 12, 0, 0)
    created = now - timedelta(days=1)
    assert is_stale(created, threshold_days=3, now=now) is False


def test_merged_pr_not_stale():
    now = datetime(2026, 6, 28, 12, 0, 0)
    created = now - timedelta(days=10)
    assert is_stale(created, threshold_days=3, pr_state="merged", now=now) is False


def test_exactly_at_threshold_not_stale():
    now = datetime(2026, 6, 28, 12, 0, 0)
    created = now - timedelta(days=3)
    assert is_stale(created, threshold_days=3, now=now) is False


def test_one_second_above_threshold_is_stale():
    now = datetime(2026, 6, 28, 12, 0, 0)
    created = now - timedelta(days=3, seconds=1)
    assert is_stale(created, threshold_days=3, now=now) is True
