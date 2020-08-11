import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

articlelist = []

def request(x):
    url = f'https://blog.mozilla.org/page/{x}/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, features='lxml')
    return soup.find_all('article', class_ = 'post-summary')

def parse(articles):
    for item in articles:
        title = item.find({'h2': 'entry-title'}).text
        date = item.find({'time': 'date published'}).text
        author = item.find({'address': 'vcard'}).text
        link = item.find({'a': 'entry-link'})
        article = {
            'title': title,
            'date': date,
            'author': author,
            'link': link['href']
        }

        articlelist.append(article)

def output():
    df = pd.DataFrame(articlelist)
    df.to_excel('articlelist.xlsx', index=False)
    print('Saved to xlsx.')

x = 1

while True:
    print(f'Page {x}')
    articles = request(x)
    x = x + 1
    time.sleep(3)
    if len(articles) != 0:
        parse(articles)
    else:
        break

print('Completed, total articles is', len(articlelist))
output()
