from ip_watch_bot.storage import read_last_ip, write_last_ip


def test_read_last_ip_returns_none_when_file_missing(tmp_path):
    path = tmp_path / "last_ip.txt"

    assert read_last_ip(path) is None


def test_write_then_read_last_ip(tmp_path):
    path = tmp_path / "last_ip.txt"

    write_last_ip(path, "203.0.113.42")

    assert read_last_ip(path) == "203.0.113.42"


def test_read_last_ip_strips_whitespace(tmp_path):
    path = tmp_path / "last_ip.txt"
    path.write_text("203.0.113.42\n")

    assert read_last_ip(path) == "203.0.113.42"


def test_write_last_ip_creates_parent_dirs(tmp_path):
    path = tmp_path / "nested" / "last_ip.txt"

    write_last_ip(path, "203.0.113.42")

    assert read_last_ip(path) == "203.0.113.42"
