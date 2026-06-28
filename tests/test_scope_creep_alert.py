"""Scope creep alert — issue created after sprint start triggers alert."""

from datetime import datetime


def is_scope_creep(issue_created_at, sprint_start_date, issue_points=None, threshold_points=6):
    if issue_created_at <= sprint_start_date:
        return False
    if threshold_points is not None and issue_points is not None:
        return issue_created_at > sprint_start_date and issue_points > threshold_points
    return issue_created_at > sprint_start_date


def test_issue_after_sprint_start_is_creep():
    sprint_start = datetime(2026, 6, 14)
    issue_created = datetime(2026, 6, 16)
    assert is_scope_creep(issue_created, sprint_start) is True


def test_issue_before_sprint_start_not_creep():
    sprint_start = datetime(2026, 6, 14)
    issue_created = datetime(2026, 6, 12)
    assert is_scope_creep(issue_created, sprint_start) is False


def test_issue_on_sprint_start_not_creep():
    sprint_start = datetime(2026, 6, 14)
    issue_created = datetime(2026, 6, 14)
    assert is_scope_creep(issue_created, sprint_start) is False


def test_issue_with_high_points_after_start_is_creep():
    sprint_start = datetime(2026, 6, 14)
    issue_created = datetime(2026, 6, 16)
    assert is_scope_creep(issue_created, sprint_start, issue_points=8, threshold_points=6) is True


def test_issue_with_low_points_after_start_not_creep():
    sprint_start = datetime(2026, 6, 14)
    issue_created = datetime(2026, 6, 16)
    assert is_scope_creep(issue_created, sprint_start, issue_points=3, threshold_points=6) is False
