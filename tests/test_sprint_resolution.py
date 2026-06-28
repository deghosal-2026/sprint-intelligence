from api.poller.compute import iso_week_range


def test_returns_12_sprints():
    sprints = iso_week_range(2026, 2, 12)
    assert len(sprints) == 12


def test_sprint_naming_format():
    sprints = iso_week_range(2026, 2, 3)
    assert sprints[0]["name"] == "2026.02.03"
    assert sprints[1]["name"] == "2026.04.05"
    assert sprints[2]["name"] == "2026.06.07"


def test_sprint_dates_are_two_weeks():
    sprints = iso_week_range(2026, 2, 1)
    s = sprints[0]
    start = s["start_date"]
    end = s["end_date"]
    delta = (end - start).days
    assert delta == 13, f"Expected 13 days (2 weeks), got {delta}"


def test_sprints_are_contiguous():
    sprints = iso_week_range(2026, 2, 4)
    for i in range(len(sprints) - 1):
        gap = (sprints[i + 1]["start_date"] - sprints[i]["end_date"]).days
        assert gap == 1, f"Gap of {gap} days between sprint {i} and {i+1}"


def test_custom_num_sprints():
    sprints = iso_week_range(2026, 2, 6)
    assert len(sprints) == 6


def test_week_numbers_in_name():
    sprints = iso_week_range(2026, 10, 2)
    assert sprints[0]["name"] == "2026.10.11"
    assert sprints[1]["name"] == "2026.12.13"


def test_year_boundary():
    sprints = iso_week_range(2025, 51, 2)
    assert sprints[0]["name"] == "2025.51.52"


def test_strptime_valid():
    sprints = iso_week_range(2026, 2, 1)
    from datetime import date
    assert isinstance(sprints[0]["start_date"], date)
