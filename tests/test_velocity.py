"""Velocity tests — test the aggregation logic directly."""


def compute_velocity(issues):
    planned = sum(i.get("story_points", 0) or 0 for i in issues)
    completed = sum(
        i.get("story_points", 0) or 0
        for i in issues
        if i.get("state") == "closed"
    )
    carry_over = sum(
        i.get("story_points", 0) or 0
        for i in issues
        if i.get("state") == "open"
    )
    ratio = round(completed / planned, 4) if planned else None
    return {"planned": planned, "completed": completed, "carry_over": carry_over, "ratio": ratio}


def test_all_closed():
    issues = [
        {"story_points": 3, "state": "closed"},
        {"story_points": 5, "state": "closed"},
        {"story_points": 2, "state": "closed"},
    ]
    v = compute_velocity(issues)
    assert v["planned"] == 10
    assert v["completed"] == 10
    assert v["carry_over"] == 0
    assert v["ratio"] == 1.0


def test_mixed_open_closed():
    issues = [
        {"story_points": 3, "state": "closed"},
        {"story_points": 5, "state": "open"},
        {"story_points": 2, "state": "closed"},
    ]
    v = compute_velocity(issues)
    assert v["planned"] == 10
    assert v["completed"] == 5
    assert v["carry_over"] == 5
    assert v["ratio"] == 0.5


def test_all_open():
    issues = [
        {"story_points": 8, "state": "open"},
        {"story_points": 5, "state": "open"},
    ]
    v = compute_velocity(issues)
    assert v["planned"] == 13
    assert v["completed"] == 0
    assert v["carry_over"] == 13
    assert v["ratio"] == 0.0


def test_no_issues():
    v = compute_velocity([])
    assert v["planned"] == 0
    assert v["completed"] == 0
    assert v["carry_over"] == 0
    assert v["ratio"] is None


def test_issues_without_points():
    issues = [
        {"story_points": None, "state": "closed"},
        {"story_points": 3, "state": "closed"},
    ]
    v = compute_velocity(issues)
    assert v["planned"] == 3
    assert v["completed"] == 3
    assert v["ratio"] == 1.0


def test_all_without_points():
    issues = [
        {"story_points": None, "state": "closed"},
        {"story_points": None, "state": "open"},
    ]
    v = compute_velocity(issues)
    assert v["planned"] == 0
    assert v["completed"] == 0
    assert v["ratio"] is None


def test_rounding():
    issues = [
        {"story_points": 3, "state": "closed"},
        {"story_points": 5, "state": "closed"},
        {"story_points": 5, "state": "open"},
    ]
    v = compute_velocity(issues)
    assert v["ratio"] == 0.6154  # 8/13


def test_large_points():
    issues = [{"story_points": 100, "state": "closed"} for _ in range(10)]
    v = compute_velocity(issues)
    assert v["planned"] == 1000
    assert v["completed"] == 1000
    assert v["ratio"] == 1.0
