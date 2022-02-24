import requests
from bs4 import BeautifulSoup
import re
import csv

CSV = 'goods.csv'
HOST = 'https://www.wildberries.ru'
URL = 'https://www.wildberries.ru/catalog/obuv/muzhskaya'
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
}

def count_time(func):
    import time

    def wrapper(*args, **kwargs):
        start = time.time()
        return_value = func(*args, **kwargs)
        end = time.time()
        print('[*] Время выполнения: {} секунд.'.format(end-start))
        return return_value
    return wrapper

def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_conteent(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='product-card')
    goods = []
    for item in items:
        good = item.find('span', class_='goods-name').get_text(strip=True)
        brand = (item.find('strong', class_='brand-name').get_text(strip=True))[:-1]
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
                'link': HOST+href
            }
        )
    return goods

def save_bd(goods, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Артикул', 'Товар', 'Бренд', 'Цена со скидкой', 'Цена без скидки', 'Ссылка на товар'])
        for item in goods:
            writer.writerow( [item['id'], item['good'], item['brand'], item['sales price'], item['full price'], item['link']])
@count_time
def parser(page: int):
        html = get_html(URL)
        if html.status_code == 200:
            goods = []
            for page in range(1, page):
                print(f'Парсим страницу № {page}')
                html = get_html(URL, params={'page': page})
                goods.extend(get_conteent(html.text))
            print(f'Выборка составила {len(goods)} товаров')
            save_bd(goods, CSV)
        else:
            print('Error')

html = get_html(URL)
parser(12)


