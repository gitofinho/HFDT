import requests

# Sending the query in the get request parameter

query = "안녕"

url = f"http://127.0.0.1:8000/ask/?query={query}"

with requests.get(url, stream=True) as r:
    for chunk in r.iter_content(1024):
        print(chunk.decode('utf-8'), end="")