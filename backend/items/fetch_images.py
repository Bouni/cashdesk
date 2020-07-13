import os
import re
import requests

from cashdesk.settings import BASE_DIR
from .models import Item

def download(u, n):
    try:
        r = requests.get(u, allow_redirects=True)
        if r.status_code != requests.codes.ok:
            return None
        path = os.path.join(BASE_DIR, "media", "items", n)
        with open(path, "wb") as f:
            f.write(r.content)
        return path
    except Exception as e:
        print(e)
        return None


def fetch():
    try:
        items = Item.objects.filter(image__istartswith='http')
        for i in items:
            ext = i.image.rsplit(".",1)[1]
            fname = f"{i.brand}-{i.name}.{ext}".replace(" ", "-")
            r = download(i.image, fname)
            if r:
                print(f"Downloaded item image {i.image} to /media/items/{fname}")
                i.image = f"/media/tems/{fname}"
                i.save()
            else:
                print(f"Error: item image {i.image} couldn't be downloaded!")
    except:
        pass
