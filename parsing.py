import requests
import csv
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

HOST = 'https://www.enzomuratore.com/'
REQUEST_URL = 'https://www.enzomuratore.com/sklep/'

STATUS_CODE_ACCEPT = 200
CSV_FILE = 'parsing-file.csv'


def fake_user_agent():
    user_agent = {
        'user-agent': UserAgent().random
    }
    return user_agent


def get_html(url, params=''):
    user_agent = fake_user_agent()
    requests_variable = requests.get(url, headers=user_agent, params=params)

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
    site = get_html(REQUEST_URL)

    if site.status_code == STATUS_CODE_ACCEPT:
        products = []
        products.extend(get_content(site.text))
        save_csv(products, CSV_FILE)
        pass
    else:
        print('ERROR')


main()
