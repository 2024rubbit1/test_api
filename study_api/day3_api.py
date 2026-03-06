import requests
url = "https://jsonplaceholder.typicode.com/posts/1"
r = requests.get(url).json()
print(r["title"])