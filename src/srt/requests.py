import requests


def lastfm_get(payload):
    headers = {"user-agent": usragent}
    url = "https://ws.audioscrobbler.com/2.0"

    payload["api_key"] = API_KEY
    payload["format"] = "json"

    response = requests.get(url, headers=headers, params=payload)
