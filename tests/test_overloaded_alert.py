"""Overloaded engineer alert — WIP > threshold triggers alert."""


def is_overloaded(wip_count, max_wip):
    return wip_count > max_wip


def test_wip_above_threshold_is_overloaded():
    assert is_overloaded(5, 4) is True


def test_wip_at_threshold_not_overloaded():
    assert is_overloaded(4, 4) is False


def test_wip_below_threshold_not_overloaded():
    assert is_overloaded(3, 4) is False


def test_wip_zero_not_overloaded():
    assert is_overloaded(0, 4) is False


def test_threshold_zero_means_all_overloaded():
    assert is_overloaded(1, 0) is True
