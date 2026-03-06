import requests
url = "https://httpbin.org/delay/5"
try:
    r = requests.get(url, timeout=3)
except requests.exceptions.Timeout as t:
    print(t)
# print(r.json()["headers"])