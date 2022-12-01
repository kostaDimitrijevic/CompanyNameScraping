import requests
from bs4 import BeautifulSoup
import pandas as pd

urls = pd.read_excel("url_list.xlsx")
print(urls['URL'].tolist())
good_urls = []
https = 'https://www.'
for url in urls['URL'].tolist():
    split = url.split('.')
    split.reverse()
    url = https
    for i, s in enumerate(split):
        if i != len(split) - 1:
            s = s + '.'
        url += s

    good_urls.append(url)
pd.DataFrame(good_urls).to_csv("urls.csv")