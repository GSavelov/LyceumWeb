import requests
import json

URL = "http://127.0.0.1:5050"


def get_group(group_id):
    try:
        response = requests.get(f"{URL}/group/{group_id}")
        return response.json()
    except requests.exceptions.ConnectionError:
        return json.dumps({"Error": "connection failed"})


def get_list_of_groups():
    try:
        response = requests.get(f"{URL}/groups")
        return response.json()
    except requests.exceptions.ConnectionError:
        return json.dumps({"Error": "connection failed"})


def get_question(question_id):
    try:
        response = requests.get(f"{URL}/question/{question_id}")
        return response.json()
    except requests.exceptions.ConnectionError:
        return json.dumps({"Error": "connection failed"})


def get_list_of_questions(group_id):
    try:
        response = requests.get(f"{URL}/questions/{group_id}")
        return response.json()
    except requests.exceptions.ConnectionError:
        return json.dumps({"Error": "connection failed"})
