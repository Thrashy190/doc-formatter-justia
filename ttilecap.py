import requests

url = "https://title-case-converter.p.rapidapi.com/v1/TitleCase"

querystring = {"title":"thanks for opting in to stay in touch","style":"<REQUIRED>"}

headers = {
	"X-RapidAPI-Key": "f5d4a132f5mshec0cef68449891fp1a5424jsn0c30122a75fa",
	"X-RapidAPI-Host": "title-case-converter.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())