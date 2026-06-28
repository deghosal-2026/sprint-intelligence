"""AI summary missing data — prompt handles null/empty metrics."""

from api.poller.prompts import sdm_summary_prompt


def test_velocity_unknown_when_no_planned():
    metrics = {
        "planned_points": 0,
        "completed_points": 0,
    }
    prompt = sdm_summary_prompt(metrics)
    assert "unknown" in prompt


def test_cycle_time_unknown_when_null():
    metrics = {
        "velocity_ratio": 0.8,
        "planned_points": 50,
        "completed_points": 40,
        "cycle_time_mean_hours": None,
    }
    prompt = sdm_summary_prompt(metrics)
    assert "unknown" in prompt


def test_no_bugs_when_none():
    metrics = {
        "velocity_ratio": 0.8,
        "planned_points": 50,
        "completed_points": 40,
        "bugs_introduced": 0,
    }
    prompt = sdm_summary_prompt(metrics)
    assert "No new bugs" in prompt


def test_empty_metrics_dict():
    prompt = sdm_summary_prompt({})
    assert "unknown" in prompt


def test_partial_metrics():
    metrics = {
        "velocity_ratio": 1.0,
        "planned_points": 30,
        "completed_points": 30,
    }
    prompt = sdm_summary_prompt(metrics)
    assert "100%" in prompt
