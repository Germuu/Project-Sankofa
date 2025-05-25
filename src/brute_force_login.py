import requests

url = "http://localhost:5000/login"
for i in range(100):
    data = {"username": "admin", "password": f"password{i}"}
    response = requests.post(url, data=data)
    print(f"Attempt {i}: {response.status_code}")