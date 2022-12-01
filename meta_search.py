from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
import pandas as pd

userAgent = UserAgent()
urls = pd.read_csv("urls.csv")
proba = urls['URL'].tolist()
companies = [[]]
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'}


def try_http(url_req):
    new_url = url_req.removeprefix('https')
    new_url = 'http' + new_url
    new_req = requests.get(new_url, allow_redirects=True, headers=headers, stream=True)
    soup_func(new_req, new_url)


def try_no_www(url_req):
    split = url_req.split('www.')
    new_url = ''
    for s in split:
        new_url += s
    try:
        new_req = requests.get(new_url, allow_redirects=True, headers=headers, stream=True)
        soup_func(new_req, new_url)
    except requests.exceptions.ConnectionError:
        try_http(new_url)


def try_com(url_req):
    split = url_req.split('.')
    new_url = ''
    for i, s in enumerate(split):
        if i != len(split) - 1:
            s = s + '.'
        else:
            s = 'com'
        new_url += s
    try:
        new_req = requests.get(new_url, allow_redirects=True, headers=headers, stream=True)
        soup_func(new_req, new_url)
    except requests.exceptions.ConnectionError:
        try_no_www(new_url)


def soup_func(request, url_new):
    soup = BeautifulSoup(request.text, 'html.parser')
    company = soup.find("meta", property="og:site_name")
    companies.append([company["content"] if company else "No meta site_name given", url_new])


for url in urls['URL'].tolist():
    if type(url) is float:
        break
    print(url)

    # headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0'}
    try:
        reqs = requests.get(url, allow_redirects=True, headers=headers, stream=True)
        soup_func(reqs, url)
    except requests.exceptions.SSLError:
        try_com(url)
    except requests.exceptions.ConnectTimeout:
        try_no_www(url)

pd.DataFrame(companies, columns=['Company name', 'URL']).to_csv("results.csv")
