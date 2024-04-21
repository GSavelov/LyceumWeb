import requests

response = requests.get('http://127.0.0.1:5050/groups').json()
print(response)