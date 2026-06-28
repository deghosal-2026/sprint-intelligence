from api.poller.fetch import parse_labels


class FakeLabelConfig:
    points_prefix = "points:"
    bug_label = "bug"
    feature_label = "feature"
    techdebt_label = "tech-debt"
    task_label = "task"
    sprint_prefix = "sprint:"


cfg = FakeLabelConfig()


def test_parses_points_label():
    labels = [{"name": "points:3"}]
    points, bug, feat, tech, task, blocked, sprint = parse_labels(labels, cfg)
    assert points == 3.0
    assert not bug


def test_parses_bug_label():
    labels = [{"name": "bug"}]
    _, bug, _, _, _, _, _ = parse_labels(labels, cfg)
    assert bug


def test_parses_feature_label():
    labels = [{"name": "feature"}]
    _, _, feat, _, _, _, _ = parse_labels(labels, cfg)
    assert feat


def test_parses_techdebt_label():
    labels = [{"name": "tech-debt"}]
    _, _, _, tech, _, _, _ = parse_labels(labels, cfg)
    assert tech


def test_parses_task_label():
    labels = [{"name": "task"}]
    _, _, _, _, task, _, _ = parse_labels(labels, cfg)
    assert task


def test_parses_blocked_label():
    labels = [{"name": "blocked"}]
    _, _, _, _, _, blocked, _ = parse_labels(labels, cfg)
    assert blocked


def test_parses_sprint_label():
    labels = [{"name": "sprint:team1-26.24.25"}]
    _, _, _, _, _, _, sprint = parse_labels(labels, cfg)
    assert sprint == "sprint:team1-26.24.25"


def test_parses_multiple_labels():
    labels = [
        {"name": "points:5"},
        {"name": "bug"},
        {"name": "sprint:team1-26.24.25"},
    ]
    points, bug, feat, tech, task, blocked, sprint = parse_labels(labels, cfg)
    assert points == 5.0
    assert bug
    assert not feat
    assert not blocked
    assert sprint == "sprint:team1-26.24.25"


def test_no_labels():
    labels = []
    points, bug, feat, tech, task, blocked, sprint = parse_labels(labels, cfg)
    assert points is None
    assert not any([bug, feat, tech, task, blocked])
    assert sprint is None


def test_points_various_values():
    for val in ["1", "2", "3", "5", "8", "13"]:
        labels = [{"name": f"points:{val}"}]
        points, *_ = parse_labels(labels, cfg)
        assert points == float(val), f"Failed for points:{val}"


def test_invalid_points_label():
    labels = [{"name": "points:abc"}]
    points, *_ = parse_labels(labels, cfg)
    assert points is None


def test_empty_labels_ignored():
    labels = [{"name": ""}, {"name": "points:3"}]
    points, *_ = parse_labels(labels, cfg)
    assert points == 3.0
