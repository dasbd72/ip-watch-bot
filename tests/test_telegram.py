from unittest.mock import Mock, patch

import pytest

from ip_detect.telegram import send_message


@patch("ip_detect.telegram.requests.post")
def test_send_message_posts_to_telegram_api(mock_post):
    mock_response = Mock()
    mock_response.raise_for_status = Mock()
    mock_post.return_value = mock_response

    send_message(token="abc123", chat_id="42", text="hello")

    mock_post.assert_called_once_with(
        "https://api.telegram.org/botabc123/sendMessage",
        data={"chat_id": "42", "text": "hello"},
        timeout=10,
    )
    mock_response.raise_for_status.assert_called_once()


@patch("ip_detect.telegram.requests.post")
def test_send_message_raises_on_http_error(mock_post):
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = Exception("boom")
    mock_post.return_value = mock_response

    with pytest.raises(Exception, match="boom"):
        send_message(token="abc123", chat_id="42", text="hello")
