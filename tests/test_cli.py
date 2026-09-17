from unittest.mock import Mock, patch

from ip_watch_bot import cli
from ip_watch_bot.config import Credentials, read_credentials, write_credentials


def parse(*argv):
    return cli.build_parser().parse_args(argv)


class TestConfigure:
    def test_configure_saves_flags_without_prompting(self):
        args = parse("configure", "--token", "abc", "--chat-id", "123")

        exit_code = cli.cmd_configure(args)

        assert exit_code == 0
        assert read_credentials() == Credentials(bot_token="abc", chat_id="123")

    @patch("builtins.input")
    def test_configure_prompts_for_missing_fields(self, mock_input):
        mock_input.side_effect = ["abc", "123"]
        args = parse("configure")

        exit_code = cli.cmd_configure(args)

        assert exit_code == 0
        assert read_credentials() == Credentials(bot_token="abc", chat_id="123")

    @patch("builtins.input")
    def test_configure_keeps_existing_value_on_blank_input(self, mock_input):
        write_credentials("old-token", "old-chat")
        mock_input.side_effect = ["", "new-chat"]
        args = parse("configure")

        exit_code = cli.cmd_configure(args)

        assert exit_code == 0
        assert read_credentials() == Credentials(
            bot_token="old-token", chat_id="new-chat"
        )

    @patch("builtins.input")
    def test_configure_fails_when_token_still_empty(self, mock_input):
        mock_input.side_effect = ["", "123"]
        args = parse("configure")

        exit_code = cli.cmd_configure(args)

        assert exit_code == 1
        assert read_credentials() == Credentials(bot_token="", chat_id="")


class TestCheck:
    @patch("ip_watch_bot.cli.run")
    def test_check_errors_when_not_configured(self, mock_run):
        args = parse("check")

        exit_code = cli.cmd_check(args)

        assert exit_code == 1
        mock_run.assert_not_called()

    @patch("ip_watch_bot.cli.run")
    def test_check_runs_when_configured(self, mock_run):
        write_credentials("abc", "123")
        args = parse("check")

        exit_code = cli.cmd_check(args)

        assert exit_code == 0
        mock_run.assert_called_once()


class TestService:
    @patch("subprocess.run")
    def test_service_enable_blocked_when_not_configured(self, mock_run):
        args = parse("service", "enable")

        exit_code = cli.cmd_service(args)

        assert exit_code == 1
        mock_run.assert_not_called()

    @patch("subprocess.run")
    def test_service_enable_passes_now_flag(self, mock_run):
        write_credentials("abc", "123")
        mock_run.return_value = Mock(returncode=0)
        args = parse("service", "enable")

        exit_code = cli.cmd_service(args)

        assert exit_code == 0
        mock_run.assert_called_once_with(
            ["systemctl", "--user", "enable", "--now", cli.TIMER_UNIT]
        )

    @patch("subprocess.run")
    def test_service_status_passes_through_without_now_flag(self, mock_run):
        mock_run.return_value = Mock(returncode=3)
        args = parse("service", "status")

        exit_code = cli.cmd_service(args)

        assert exit_code == 3
        mock_run.assert_called_once_with(
            ["systemctl", "--user", "status", cli.TIMER_UNIT]
        )
