from unittest.mock import Mock, patch

import pytest

from ip_watch_bot.ip import get_public_ip


@patch("ip_watch_bot.ip.requests.get")
def test_get_public_ip_returns_stripped_ip(mock_get):
    mock_response = Mock()
    mock_response.text = "203.0.113.42\n"
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    ip = get_public_ip()

    assert ip == "203.0.113.42"
    mock_get.assert_called_once()


@patch("ip_watch_bot.ip.requests.get")
def test_get_public_ip_raises_on_http_error(mock_get):
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = Exception("boom")
    mock_get.return_value = mock_response

    with pytest.raises(Exception, match="boom"):
        get_public_ip()
