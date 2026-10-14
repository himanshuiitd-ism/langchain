import os, requests

KEY = os.getenv("SORSA_KEY")
BASE = "https://api.sorsa.io/v3"
handles = open("listed.txt").read().split()

r = requests.get(f"{BASE}/info-batch", headers={"ApiKey": KEY},
                 params={"usernames": handles}, timeout=20)
r.raise_for_status()
users = r.json()["users"]

print("asked:", len(handles), "got:", len(users))
for u in users:
    print(f'{u["username"]:<18} followers={u["followers_count"]:<7} following={u["followings_count"]}')
missing = {h.lower() for h in handles} - {u["username"].lower() for u in users}
print("missing:", sorted(missing))