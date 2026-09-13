from pathlib import Path


def read_last_ip(path: Path) -> str | None:
    if not path.exists():
        return None
    return path.read_text().strip() or None


def write_last_ip(path: Path, ip: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(ip)
