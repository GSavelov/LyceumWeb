import requests
import json
from bot_requests import URL

with open("questions.json", encoding='utf-8') as questions:
    data = json.load(questions)
    for params in data:
        requests.post(f'{URL}/questions', json=params)

with open("groups.json", encoding='utf-8') as groups:
    data = json.load(groups)
    for params in data:
        requests.post(f'{URL}/groups', json=params)
