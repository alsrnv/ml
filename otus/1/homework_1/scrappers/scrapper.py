import logging
import requests
from bs4 import BeautifulSoup
import pandas as pd

logger = logging.getLogger(__name__)


class Scrapper(object):
    def __init__(self, skip_objects=None):
        self.skip_objects = skip_objects

    def get_html(self, url):
        logger.info("get_html")
        """Функция возвращает html страницу"""
        response = requests.get(url)
        if not response.ok:
            logger.error(response.text)
        else:
            return response.text

    def get_integer_from_string(self, string):
        """Вспомогательная функция. Из строки вытаскивает число"""
        output = "".join(string.split())
        output = int(''.join(x for x in output if x.isdigit()))
        return int(output)

    def get_total_pages(self, html):
        logger.info("get_total_pages")
        """Функция возвращает номер конечной страницы """
        soup = BeautifulSoup(html, 'lxml')
        # Получаем ссылку на последнюю страницу. Пример - '/moskva/avtomobili/toyota?p=60&radius=0'
        try:
            pages = soup.find('div', class_ = 'pagination-pages').find_all('a', class_ = 'pagination-page')[-1].get('href')
            left_border, right_border = pages.find('p='), pages.find('&radius')
            total_pages = int(pages[left_border + 2: right_border])
            logger.info("total_pages is " + str(total_pages))
        except Exception as e:
            logger.error('Ошибка в получении номера последней страницы')
            logger.error(e)
            raise
        return total_pages

    def get_page_data(self, html):
        output = pd.DataFrame()
        soup = BeautifulSoup(html, 'lxml')
        ads = soup.find('div', class_ = 'js-catalog_after-ads').find_all('div', class_ = 'item_table')
        for ad in ads:
            try:
                title = ad.find('a', class_ = 'item-description-title-link').text
                car_name, car_year = title.split(',')[0].strip(), title.split(',')[1].strip()
            except:
                car_name, car_year = '', ''
            try:
                price = ad.find('div', class_ = 'about').find('span', class_ = 'price').text
                price = self.get_integer_from_string(price)
            except:
                price = ''
            try:
                info = ad.find('div', class_ = 'about').find('div', class_ = 'specific-params specific-params_block').text
                info = info.replace(u'\xa0', u' ').strip().split(',')

                car_distance = self.get_integer_from_string(info[0])
                car_shape = info[2]
                car_main_wheel = info[3]
                car_oil_type = info[4]
                car_volume = info[1].split('(')[0].split()[0]
                car_transmission = info[1].split('(')[0].split()[1]
                car_horse = self.get_integer_from_string(info[1].split('(')[1])

            except:
                info = ''

            output = pd.concat([output, pd.DataFrame({
                                'car_name':[car_name],
                                'car_year':[car_year],
                                'car_price':[price],
                                'car_distance':[car_distance],
                                'car_shape':[car_shape],
                                'car_main_wheel':[car_main_wheel],
                                'car_oil_type':[car_oil_type],
                                'car_volume':[car_volume],
                                'car_transmission':[car_transmission],
                                'car_horse':[car_horse]})])
        return output




    # def scrap_process(self, storage):

    #     # You can iterate over ids, or get list of objects
    #     # from any API, or iterate throught pages of any site
    #     # Do not forget to skip already gathered data
    #     # Here is an example for you
    #     url = 'https://otus.ru/'
    #     response = requests.get(url)

    #     if not response.ok:
    #         logger.error(response.text)
    #         # then continue process, or retry, or fix your code

    #     else:
    #         # Note: here json can be used as response.json
    #         data = response.text

    #         # save scrapped objects here
    #         # you can save url to identify already scrapped objects
    #         storage.write_data([url + '\t' + data.replace('\n', '')])
