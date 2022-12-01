
import requests
from bs4 import BeautifulSoup
import pandas as pd


urls = pd.read_csv("results.csv")
proba = urls['URL'].tolist()
companies = [[]]
headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN) AppleWebKit/533+ (KHTML, like Gecko)'}

for name, url in zip(urls['Company name'].tolist(), urls['URL'].tolist()):
    if name == 'No meta site_name given':
        if type(url) is float:
            break
        print(url)
        # headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0'}
        reqs = requests.get(url, allow_redirects=True, headers=headers, stream=True)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        if soup.find("head") is not None:
            company = soup.find("head").find("title")
            if company and len(company.contents) > 0:
                companies.append([company.contents[0], url])
            else:
                companies.append(['Not found', url])
    else:
        companies.append([name, url])

pd.DataFrame(companies, columns=['Company name', 'URL']).to_csv("final.csv")
