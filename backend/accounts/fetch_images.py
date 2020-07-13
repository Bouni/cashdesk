import os
import re
import requests

from cashdesk.settings import BASE_DIR
from .models import Account

def download(u, n):
    try:
        r = requests.get(u, allow_redirects=True)
        if r.status_code != requests.codes.ok:
            return None
        path = os.path.join(BASE_DIR, "media", "owners", n)
        with open(path, "wb") as f:
            f.write(r.content)
        return path
    except Exception as e:
        print(e)
        return None


def fetch():
    try:
        accounts = Account.objects.all()
        for a in accounts:
            fname = f"{a.owner}.svg"
            if not os.path.isfile(os.path.join(BASE_DIR, "media", "owners", fname)):
                url = f"https://avatars.dicebear.com/api/bottts/{a.owner}.svg"
                r = download(url, fname)
                print(f"Downloaded owner image to /media/owners/{a.owner}.svg")
    except:
        pass

