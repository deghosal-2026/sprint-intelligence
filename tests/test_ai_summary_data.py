"""AI summary data points — prompt includes expected metrics."""

from api.poller.prompts import sdm_summary_prompt, SDM_SUMMARY_SYSTEM


def test_prompt_contains_velocity():
    metrics = {
        "velocity_ratio": 0.8,
        "planned_points": 50,
        "completed_points": 40,
        "cycle_time_mean_hours": 24.0,
        "cycle_time_median_hours": 20.0,
        "bugs_introduced": 3,
        "capacity_ratio": 0.75,
        "carry_over_points": 10,
    }
    prompt = sdm_summary_prompt(metrics)
    assert "80%" in prompt
    assert "40/50" in prompt


def test_prompt_contains_cycle_time():
    metrics = {
        "velocity_ratio": 0.8,
        "planned_points": 50,
        "completed_points": 40,
        "cycle_time_mean_hours": 24.0,
        "cycle_time_median_hours": 20.0,
        "bugs_introduced": 3,
        "capacity_ratio": 0.75,
        "carry_over_points": 10,
    }
    prompt = sdm_summary_prompt(metrics)
    assert "24.0h" in prompt


def test_prompt_contains_bugs():
    metrics = {
        "velocity_ratio": 0.8,
        "planned_points": 50,
        "completed_points": 40,
        "cycle_time_mean_hours": 24.0,
        "bugs_introduced": 3,
    }
    prompt = sdm_summary_prompt(metrics)
    assert "3" in prompt


def test_prompt_contains_capacity():
    metrics = {
        "velocity_ratio": 0.8,
        "planned_points": 50,
        "completed_points": 40,
        "cycle_time_mean_hours": 24.0,
        "capacity_ratio": 0.75,
    }
    prompt = sdm_summary_prompt(metrics)
    assert "75%" in prompt


def test_prompt_contains_carry_over():
    metrics = {
        "velocity_ratio": 0.6,
        "planned_points": 50,
        "completed_points": 30,
        "cycle_time_mean_hours": 24.0,
        "carry_over_points": 20,
    }
    prompt = sdm_summary_prompt(metrics)
    assert "20" in prompt


def test_system_prompt_has_rules():
    assert "5 bullet points" in SDM_SUMMARY_SYSTEM
    assert "metric → consequence" in SDM_SUMMARY_SYSTEM
    assert "Data unavailable" in SDM_SUMMARY_SYSTEM
