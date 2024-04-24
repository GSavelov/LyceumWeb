import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
URL = os.getenv('URL')


def add_users():
    with open("users.json", encoding='utf-8') as users:
        data = json.load(users)
        for params in data:
            requests.post(f'{URL}/users', json=params)


def add_questions():
    with open("questions.json", encoding='utf-8') as questions:
        data = json.load(questions)
        for params in data:
            requests.post(f'{URL}/questions', json=params)


def add_groups():
    with open("groups.json", encoding='utf-8') as groups:
        data = json.load(groups)
        for params in data:
            requests.post(f'{URL}/groups', json=params)


if __name__ == '__main__':
    add_users()
    add_questions()
    add_groups()
