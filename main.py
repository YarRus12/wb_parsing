import requests
from bs4 import BeautifulSoup
import re
import csv

HOST = 'https://www.wildberries.ru/'
URL = 'https://www.wildberries.ru/catalog/obuv/muzhskaya'
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
}

def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_conteent(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='product-card')
    goods = []
    for item in items:
        good = item.find('span', class_='goods-name').get_text(strip=True)
        brand = item.find('strong', class_='brand-name').get_text(strip=True)
        low_price = str(item.find('ins', class_='lower-price'))
        low_price = "".join([s for s in re.findall(r'-?\d+\.?\d*', low_price)])
        full_price = str(item.find('span', class_='price-old-block'))
        full_price = "".join([s for s in re.findall(r'-?\d+\.?\d*', full_price)])
        id = item.find('div', class_='product-card__wrapper').find('a').get('href')
        id = "".join([s for s in re.findall(r'-?\d+\.?\d*', id)])
        href = item.find('div', class_='product-card__wrapper').find('a').get('href')

        goods.append(
            {
                'id' : id,
                'good': good,
                'brand': brand,
                'sales price': low_price,
                'full price': full_price,
                'ссылка': HOST+href
            }
        )
    return goods



html = get_html(URL)
print(*get_conteent(html.text))

