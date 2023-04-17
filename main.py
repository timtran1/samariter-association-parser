import requests as r
from bs4 import BeautifulSoup
import json

print('Fetching search page...')
search_page_url = 'https://www.samariter.ch/de/samaritervereine'
search_page = r.get(search_page_url)
soup = BeautifulSoup(search_page.text, 'html.parser')
last_page_btn = soup.find('a', {'title': 'Zur letzten Seite'})
href = last_page_btn['href']
last_page = int(href[href.rfind('=') + 1:])
print(f'{last_page} pages to fetch')

api_url = 'https://www.samariter.ch/de/views/ajax?_wrapper_format=drupal_ajax'
headers = {
    'origin': 'https://www.samariter.ch',
    'referer': 'https://www.samariter.ch/de/samaritervereine',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}
associations = []

for page in range(0, last_page):
    print(f'Fetching page {page + 1} of {last_page} (index {page})...')
    form_data = {
        'view_name': 'association_search',
        'view_display_id': 'block_search',
        'page': page,
        '_drupal_ajax': 1,
    }
    res = r.post(api_url, headers=headers, data=form_data)
    data = res.json()
    html = data[3]['data']
    soup = BeautifulSoup(html, 'html.parser')

    for article in soup.find_all('article'):
        url = None
        url_div = article.find('div', {'class': 'field--name-field-association-website'})
        if url_div:
            url = url_div.find('a')['href']

        associations.append({
            'name': article.find('div', {'class': 'field--name-field-association-name-official'}).text,
            'url': url
        })

print(associations)
# convert to csv
with open('associations.csv', 'w') as f:
    f.write('name,url\n')
    for association in associations:
        f.write(f'{association["name"]},{association["url"]}\n')

