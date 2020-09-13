import os
from bs4 import BeautifulSoup
import requests
import time


def fetch(title_keywords=[], journal_keywords=[]):
    if not os.path.exists('articles'):
        os.makedirs('articles')

    if not os.path.exists('api_key.txt'):
        print('Please construct a Springer API application.')
        print('Then past your API key in api_key.txt.')

    with open('api_key.txt', 'r') as f:
        api_key = f.read()

    params = [f'title:"{title}"' for title in title_keywords]

    if len(journal_keywords) != 0:
        params += [f'journal:"{journal}"' for journal in journal_keywords]

    page = 1
    page_size = 10
    count = 0

    url = 'http://api.springer.com/openaccess/jats'
    url += f'?api_key={api_key}&q=({" OR ".join(params)})&p={page_size}'

    response = BeautifulSoup(requests.get(url + f'&s={page}').text,
                             'lxml')

    titles = []

    while response.find('recordsdisplayed').contents[0] != '0':
        for article in response.findAll('article'):
            titles.append(article.find('article-title').contents[0])
            with open(f'articles/{count}.txt', 'w+') as f:
                f.write(str(article))
            count += 1
        time.sleep(5)

        page += page_size
        response = BeautifulSoup(requests.get(url + f'&s={page}').text,
                                 'lxml')

    print('Found the following articles:')
    for title in titles:
        print(title)


if __name__ == "__main__":
    title_keywords = ['antibiotics',
                      'antibiotic combinations',
                      'antibiotic synergy',
                      'antibiotic antagonism',
                      'antibacterial combinations',
                      'antibiotic checkerboard',
                      'antibiotic adjuvant',
                      'antibiotic potentiation',
                      'antibiotic combination screen']

    fetch(title_keywords=title_keywords)
