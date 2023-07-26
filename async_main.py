import requests
import datetime
import csv
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re
import aiohttp
import aiofiles
import asyncio
from aiocsv import AsyncWriter


async def collect_data():
    cur_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')

    ua = UserAgent()
    # print(ua.random)

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,'
                  'image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'User-Agent': ua.random
    }

    async with aiohttp.ClientSession() as session:

        # Сначала получаем страницу с номером 1
        response = await session.get(url='https://www.atbmarket.com/promo/unikalni_propozytsiyi_vid_atb',
                                     headers=headers)
        # # Затем получаем страницу с номером 2
        response2 = await session.get(url='https://www.atbmarket.com/promo/unikalni_propozytsiyi_vid_atb?page=2',
                                      headers=headers)


        soup = BeautifulSoup(await response.text(), 'lxml')

        cards = soup.find_all('article', class_='catalog-item js-product-container')
        data_time = soup.find('div', class_='actions-timer')['data-time']


        data = []
        for card in cards:
            card_title = card.find(class_='catalog-item__info').text.strip()
            # print(card_title)

            try:
                discount_span = card.find('span', class_='custom-product-label')
                discount_text = discount_span.text.strip()
                discount_percent = re.search(r'-?(\d+)%', discount_text).group(1)
                # print(discount_percent)
            except AttributeError:
                discount_percent = '0'

            try:
                card_price_bottom = card.find('data', class_='product-price__bottom').text.strip()
                card_old_price = f'{card_price_bottom}'
                # print(card_old_price)
            except AttributeError:
                card_old_price = ''


            card_price_top = card.find('data', class_='product-price__top')['value']
            card_new_price = f'{card_price_top}'

            data.append(
                [card_title, card_old_price, card_new_price, discount_percent, data_time]
            )

    async with aiofiles.open(f'ATB_{cur_time}.csv', 'w', encoding='utf-8') as file:
        writer = AsyncWriter(file)

        await writer.writerow(
            [
                'Product',
                'Old price',
                'New price',
                'Discount',
                'Promotion time expires',
            ]
        )
        await writer.writerows(
            data
        )
    return f'ATB_{cur_time}.csv'


async def main():
    await collect_data()


if __name__ == '__main__':
    asyncio.run(main())

