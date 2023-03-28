import logging
import time

import pandas as pd
import requests
from fake_useragent import UserAgent

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s, %(levelname)s, %(name)s, %(message)s',
    handlers=[logging.FileHandler('work_logs.log', mode='w', encoding='utf-8'),
              logging.StreamHandler()]
)


def xlsx_writer(data, file_nam='result.xlsx', sheet_name='wildberries'):
    """Записывает данные в .xlsx документ."""
    df = pd.DataFrame(data)
    df.to_excel(file_nam, index=False, sheet_name=sheet_name)


def load_vender_code():
    """Загружает список артикулов."""
    try:
        with open('task_parsing.txt', 'r') as open_file:
            lines = [int(result.strip()) for result in open_file.readlines()]
        if lines:
            return lines
        raise ValueError('Добавьте хотя бы 1 артикул в "task_parsing.txt"')
    except FileNotFoundError:
        logging.critical('Отсутствует файл "task_parsing.txt"')
    except ValueError:
        logging.critical('Можно добавлять только числовые артикулы!')


def parsing_product(delay_vendor=0.5):
    """Поиск и агрегация данных о товаре."""
    results = {
        'Артикул': [],
        'Название': [],
        'Брэнд': [],
        'Стоимость': [],
        'Размер скидки': [],
        'Размер СПП': [],
        'URL товара': [],
        'Количество отзывов': [],
        'Рейтинг': [],
    }
    load_data = load_vender_code()
    if load_data:
        for vendor_code in load_data:
            time.sleep(delay_vendor)
            logging.info(f'Выполняю поиск данных по артикулу: {vendor_code}.')
            headers = {'user-agent': UserAgent(use_external_data=True).chrome}
            response = requests.get(url=f'https://card.wb.ru/cards/detail'
                                        f'?spp=18&locale=ru&lang=ru&curr=rub'
                                        f'&nm={vendor_code}', headers=headers)

            if response.status_code == 200:
                json_data = response.json().get('data')
                if json_data:
                    for product in json_data.get('products'):
                        results['Артикул'].append(vendor_code)
                        results['Название'].append(product.get('name'))
                        results['Брэнд'].append(product.get('brand'))
                        results['Стоимость'].append(product.get('priceU'))
                        results['Размер скидки'].append(
                            product.get('extended').get('basicSale')
                        )
                        results['Размер СПП'].append(
                            product.get('extended').get('clientSale')
                        )
                        results['URL товара'].append(
                            f'https://www.wildberries.ru/catalog/'
                            f'{vendor_code}/detail.aspx'
                        )
                        results['Количество отзывов'].append(
                            product.get('feedbacks')
                        )
                        results['Рейтинг'].append(product.get('rating'))

            else:
                logging.warning(f'Проблемы с получением данных, '
                                f'артикул {vendor_code}')
        xlsx_writer(results)
    else:
        logging.critical('Ошибка загрузки данных!')


parsing_product()
