import os, re, time, requests

SORSA_KEY = os.getenv("SORSA_KEY")
MY_HANDLE = "Himanshu_iitdev"
HANDLE_RE = re.compile(r"[A-Za-z0-9_]{1,15}")
DAILY_CAP = 150                               # max Sorsa calls per day
_budget = {"day": None, "used": 0}
_recent_no = {}                               # handle -> time of last "no"

def _sorsa_follows_me(handle):
    r = requests.post(
        "https://api.sorsa.io/v3/check-follow",
        headers={"ApiKey": SORSA_KEY, "Content-Type": "application/json"},
        json={"username_1": MY_HANDLE, "username_2": handle},
        timeout=10,
    )
    r.raise_for_status()
    d = r.json()
    return bool(d.get("follow")), bool(d.get("user_protected"))

def verify(handle, followers_cache):
    """followers_cache: set of lowercase handles from your weekly list.
    Returns 'yes', 'no', 'private', or 'busy'."""
    handle = handle.lstrip("@").strip()
    if not HANDLE_RE.fullmatch(handle):
        return "no"
    h = handle.lower()
    if h in followers_cache:                       # free
        return "yes"
    if time.time() - _recent_no.get(h, 0) < 120:   # don't re-check within 2 min
        return "no"
    today = time.strftime("%Y-%m-%d")
    if _budget["day"] != today:
        _budget.update(day=today, used=0)
    if _budget["used"] >= DAILY_CAP:
        return "busy"
    _budget["used"] += 1
    try:
        follows, protected = _sorsa_follows_me(handle)
    except requests.RequestException:
        return "busy"                              # show "try again in a minute"
    if follows:
        followers_cache.add(h)                     # also save to your DB
        return "yes"
    _recent_no[h] = time.time()
    return "private" if protected else "no"


if __name__ == "__main__":
    print(verify("Weaver_of_tale", set()))