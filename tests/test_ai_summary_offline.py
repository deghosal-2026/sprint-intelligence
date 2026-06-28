"""AI summary offline — graceful skip when omlx unavailable."""

from unittest.mock import patch
from api.poller.ollama_client import is_available, chat


def test_is_available_returns_false_when_offline():
    with patch("requests.get") as mock_get:
        mock_get.side_effect = ConnectionError("refused")
        assert is_available() is False


def test_is_available_returns_false_on_non_200():
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 401
        assert is_available() is False


def test_is_available_returns_true():
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        assert is_available() is True


def test_chat_returns_none_when_offline():
    with patch("requests.post") as mock_post:
        mock_post.side_effect = ConnectionError("refused")
        result = chat("Hello")
        assert result is None
