import requests

IPIFY_URL = "https://api.ipify.org"


def get_public_ip() -> str:
    response = requests.get(IPIFY_URL, timeout=10)
    response.raise_for_status()
    return response.text.strip()
