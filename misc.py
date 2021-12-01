import requests
from config import COOKIE


def get_input(url):
    resp = requests.get(url, headers={"cookie": COOKIE})
    if resp.status_code != 200:
        raise Exception(f"resp.status_code")
    return resp.content
