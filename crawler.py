import requests 
import re
from bs4 import BeautifulSoup

response = requests.get("https://www.moseleycollins.com/sitemap.xml")

soup = BeautifulSoup(response.content,"html.parser")

urls = soup.find_all("loc")
for url in urls:

    page = BeautifulSoup(requests.get(url.get_text()).content,"html.parser")

    match = re.search(r'\b5 Centerpointe Dr #400\b',str(page))

    print(f"Find:{match} page:{url.get_text()}")
