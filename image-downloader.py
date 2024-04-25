import requests 
import shutil

path = "imagen.png"
r = requests.get("https://www.washingtonstateattorneys.com/images/badges/01/01.png")

if r.status_code == 200:
    with open(path, 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)    