"""Rate limiting tests — test the rate limit sleep and retry logic."""

import time
from unittest.mock import MagicMock, patch
from api.poller.github_client import rate_limit_sleep, fetch_paginated, get_rate_limit_remaining


class TestRateLimitSleep:
    def test_above_threshold_no_sleep(self):
        resp = MagicMock()
        resp.headers = {"X-RateLimit-Remaining": "500"}
        start = time.time()
        rate_limit_sleep(resp)
        elapsed = time.time() - start
        assert elapsed < 0.5, "Should not sleep when remaining > 50"

    def test_below_threshold_sleeps(self):
        resp = MagicMock()
        resp.headers = {
            "X-RateLimit-Remaining": "10",
            "X-RateLimit-Reset": str(int(time.time()) + 2),
        }
        start = time.time()
        rate_limit_sleep(resp)
        elapsed = time.time() - start
        assert elapsed >= 1.0, "Should sleep when remaining < 50"

    def test_missing_headers(self):
        resp = MagicMock()
        resp.headers = {}
        start = time.time()
        remaining = rate_limit_sleep(resp)
        elapsed = time.time() - start
        assert remaining == 100
        assert elapsed < 0.5


class TestFetchPaginated:
    @patch("api.poller.github_client.requests.get")
    def test_single_page(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            headers={"X-RateLimit-Remaining": "500"},
            json=lambda: [{"id": 1}, {"id": 2}],
        )
        results = fetch_paginated("https://api.github.com/test")
        assert len(results) == 2

    @patch("api.poller.github_client.requests.get")
    def test_rate_limit_retry(self, mock_get):
        rate_limited = MagicMock(
            status_code=403,
            headers={
                "X-RateLimit-Remaining": "0",
                "X-RateLimit-Reset": str(int(time.time()) + 1),
            },
            text="rate limit exceeded",
        )
        ok_resp = MagicMock(
            status_code=200,
            headers={"X-RateLimit-Remaining": "500"},
            json=lambda: [{"id": 1}],
        )
        mock_get.side_effect = [rate_limited, ok_resp]
        start = time.time()
        results = fetch_paginated("https://api.github.com/test")
        elapsed = time.time() - start
        assert len(results) == 1
        assert elapsed >= 1.0, "Should retry after rate limit sleep"

    @patch("api.poller.github_client.requests.get")
    def test_404_returns_empty(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=404,
            headers={"X-RateLimit-Remaining": "500"},
        )
        results = fetch_paginated("https://api.github.com/not-found")
        assert results == []


class TestGetRateLimitRemaining:
    @patch("api.poller.github_client.requests.get")
    def test_returns_remaining(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: {"resources": {"core": {"remaining": 4321}}},
        )
        remaining = get_rate_limit_remaining()
        assert remaining == 4321

    @patch("api.poller.github_client.requests.get")
    def test_api_error_returns_zero(self, mock_get):
        mock_get.side_effect = Exception("Connection error")
        remaining = get_rate_limit_remaining()
        assert remaining == 0

    @patch("api.poller.github_client.requests.get")
    def test_bad_json_returns_zero(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: {},
        )
        remaining = get_rate_limit_remaining()
        assert remaining == 0
