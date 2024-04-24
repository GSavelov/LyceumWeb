import os
import requests
from dotenv import load_dotenv

load_dotenv()
URL = os.getenv('URL')


def get_group(group_id):
    try:
        response = requests.get(f"{URL}/group/{group_id}")
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"Error": "connection failed"}


def get_list_of_groups():
    try:
        response = requests.get(f"{URL}/groups")
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"Error": "connection failed"}


def get_question(question_id):
    try:
        response = requests.get(f"{URL}/question/{question_id}")
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"Error": "connection failed"}


def get_list_of_questions():
    try:
        response = requests.get(f"{URL}/questions")
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"Error": "connection failed"}
