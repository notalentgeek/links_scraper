import requests
from bs4 import BeautifulSoup

url = "https://shopee.tw"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    print("=====")
    # print(soup)
    print(soup.title)
    print(soup.title.string)
    print("=====")
else:
    print("Failed to retrieve the webpage.")
