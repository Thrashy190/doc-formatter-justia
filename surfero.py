import requests


urls = ["https://images.surferseo.art/ba48a270-40bc-4230-bd45-b2bd6faccfe4.jpeg",
        "https://images.surferseo.art/0775338b-ff28-4b26-8b78-b44d4c898765.jpeg",
   ]

for url in urls:
    img_data = requests.get(url).content
    name = url.split("/")[-1].split(".")[0]+".jpg"
    print("photos/"+name)
    with open(name, 'wb') as handler:
        handler.write(img_data)