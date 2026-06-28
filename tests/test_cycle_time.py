from datetime import datetime, timezone
from api.poller.fetch import compute_cycle_time


def test_cycle_time_known_hours():
    first = "2026-06-01T10:00:00Z"
    merged = "2026-06-01T18:30:00Z"
    result = compute_cycle_time(first, merged)
    assert result == 8.5, f"Expected 8.5h, got {result}"


def test_cycle_time_full_day():
    first = "2026-06-01T09:00:00Z"
    merged = "2026-06-02T09:00:00Z"
    result = compute_cycle_time(first, merged)
    assert result == 24.0, f"Expected 24.0h, got {result}"


def test_cycle_time_multiple_days():
    first = "2026-06-01T00:00:00Z"
    merged = "2026-06-04T12:00:00Z"
    result = compute_cycle_time(first, merged)
    assert result == 84.0, f"Expected 84.0h, got {result}"


def test_cycle_time_null_first_commit():
    result = compute_cycle_time(None, "2026-06-01T18:00:00Z")
    assert result is None


def test_cycle_time_null_merged():
    result = compute_cycle_time("2026-06-01T10:00:00Z", None)
    assert result is None


def test_cycle_time_both_null():
    result = compute_cycle_time(None, None)
    assert result is None


def test_cycle_time_empty_strings():
    result = compute_cycle_time("", "2026-06-01T18:00:00Z")
    assert result is None


def test_cycle_time_invalid_dates():
    result = compute_cycle_time("not-a-date", "2026-06-01T18:00:00Z")
    assert result is None
