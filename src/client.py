import requests as r

base = "http://127.0.0.1:8000"

f = r.post(f"{base}/join", json={"id": 1, "timestamp": 0, "username": "22"})
print(f.status_code)
token = f.json()["token"]
print(token)

f = r.get(
    f"{base}/events",
    json={
        "token": token,
    },
)
print(f.json())

print(f.status_code)
print(f.text)
