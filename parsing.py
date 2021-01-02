import requests
import csv
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

STATUS_CODE_ACCEPT = 200
REQUEST_URL = 'https://www.enzomuratore.com/sklep/'
CSV_FILE = 'csv/parsing-file.csv'
NEED_INFO = (
    'title',
    'available',
    'check-link'
)


def fake_useragent():
    user_agent = {
        'user-agent': UserAgent().random
    }
    return user_agent


def get_html(url, params=''):
    useragent_update = fake_useragent()
    requests_variable = requests.get(url, headers=useragent_update, params=params)
    if requests_variable.status_code == STATUS_CODE_ACCEPT:
        requests_variable = requests_variable.text
        pass
    else:
        print('ERROR')

    return requests_variable


def get_content(html):
    products_variable = []
    soup_variable = BeautifulSoup(html, 'html.parser')
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
        writer.writerow(NEED_INFO)

        for item in items:
            writer.writerow([item['title'], item['available'], item['check-link']])


def main():
    site = get_html(REQUEST_URL)
    products = []
    products.extend(get_content(site))
    save_csv(products, CSV_FILE)


main()
