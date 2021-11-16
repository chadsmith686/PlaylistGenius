import requests
from secret import API_SECRET_KEY, USER_AGENT

headers = {
    'user-agent': USER_AGENT
}

payload = {
    'api_key': API_SECRET_KEY,
    'method': 'track.getSimilar',
    'format': 'json'
}

r = requests.get('https://ws.audioscrobbler.com/2.0/', headers=headers, params=payload)
r.status_code