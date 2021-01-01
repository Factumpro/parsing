import requests
import csv
from bs4 import BeautifulSoup

HOST = 'https://www.enzomuratore.com/'
URL = 'https://www.enzomuratore.com/sklep/'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/89.0.4374.0 Mobile Safari/537.36 '
}

STATUS_ACCEPT = 200
CSV_FILE = 'parsing-file.csv'


def get_html(url, params=''):
    requests_variable = requests.get(url, headers=HEADERS, params=params)
    return requests_variable


def get_content(html):
    soup_variable = BeautifulSoup(html, 'html.parser')
    products_variable = []
    search_variable = soup_variable.find_all('li', class_='product')

    for item in search_variable:
        products_variable.append(
            {
                'title': item.find('h2', class_='woocommerce-loop-product__title').get_text(),
                'available': item.find('div', class_='ribbon-unavailable').get_text(),
                'check-link': item.find('a').get('href')
            }
        )
    return products_variable


def save_csv(items, path):
    with open(path, 'w', newline='', encoding='UTF-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['title', 'available', 'check-link'])

        for item in items:
            writer.writerow([item['title'], item['available'], item['check-link']])


def main():
    site = get_html(URL)

    if site.status_code == STATUS_ACCEPT:
        products = []
        products.extend(get_content(site.text))
        save_csv(products, CSV_FILE)
        pass
    else:
        print('ERROR')


main()
