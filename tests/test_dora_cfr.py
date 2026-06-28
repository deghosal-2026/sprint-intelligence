"""DORA CFR — change failure rate computed correctly."""


def compute_cfr(failed_incidents, total_deploys):
    return round(failed_incidents / total_deploys, 4) if total_deploys else None


def test_no_failures():
    assert compute_cfr(0, 10) == 0.0


def test_some_failures():
    assert compute_cfr(3, 10) == 0.3


def test_all_failures():
    assert compute_cfr(10, 10) == 1.0


def test_no_deploys_returns_none():
    assert compute_cfr(0, 0) is None


def test_single_deploy_no_fail():
    assert compute_cfr(0, 1) == 0.0


def test_single_deploy_fail():
    assert compute_cfr(1, 1) == 1.0


def test_rounding():
    assert compute_cfr(1, 3) == 0.3333
