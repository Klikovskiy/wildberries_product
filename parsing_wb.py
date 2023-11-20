import logging
import time
from typing import List, Dict, Union

import pandas as pd
import requests
from fake_useragent import UserAgent

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s, %(levelname)s, %(name)s, %(message)s',
    handlers=[logging.FileHandler('work_logs.log', mode='w', encoding='utf-8'),
              logging.StreamHandler()]
)


def xlsx_writer(data: Dict[str, List[Union[int, str, float]]],
                file_name: str = 'result.xlsx',
                sheet_name: str = 'wildberries') -> None:
    """Записывает данные в .xlsx документ."""
    df = pd.DataFrame(data)
    df.to_excel(file_name, index=False, sheet_name=sheet_name)


def load_vendor_codes(file_path: str = 'task_parsing.txt') -> List[int]:
    """Загружает список артикулов."""
    try:
        with open(file_path, 'r') as open_file:
            lines = [int(result.strip()) for result in open_file.readlines()]
        if lines:
            return lines
        raise ValueError('Добавьте хотя бы 1 артикул в "task_parsing.txt"')
    except FileNotFoundError:
        logging.critical(f'Отсутствует файл "{file_path}"')
    except ValueError:
        logging.critical('Можно добавлять только числовые артикулы!')


def parse_product(delay_vendor: float = 0.5) -> None:
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
    NOT_FOUND_NUMBER: int = 0
    NOT_FOUND_STRING: int = 0

    vendor_codes = load_vendor_codes()
    if vendor_codes:
        for vendor_code in vendor_codes:
            time.sleep(delay_vendor)
            logging.info(f'Выполняю поиск данных по артикулу: {vendor_code}.')
            headers = {'user-agent': UserAgent(use_external_data=True).chrome}
            response = requests.get(url=f'https://card.wb.ru/cards/detail'
                                        f'?spp=18&locale=ru&lang=ru&curr=rub'
                                        f'&nm={vendor_code}', headers=headers)

            try:
                response.raise_for_status()
                json_data = response.json().get('data')
                if json_data:
                    for product in json_data.get('products'):
                        results['Артикул'].append(vendor_code)
                        results['Название'].append(
                            product.get('name', NOT_FOUND_STRING))
                        results['Брэнд'].append(
                            product.get('brand', NOT_FOUND_STRING))
                        results['Стоимость'].append(
                            product.get('priceU', NOT_FOUND_STRING))
                        results['Размер скидки'].append(
                            product.get('extended', {}).get('basicSale',
                                                            NOT_FOUND_NUMBER)
                        )
                        results['Размер СПП'].append(
                            product.get('extended', {}).get('clientSale',
                                                            NOT_FOUND_NUMBER)
                        )
                        results['URL товара'].append(
                            f'https://www.wildberries.ru/catalog/'
                            f'{vendor_code}/detail.aspx'
                        )
                        results['Количество отзывов'].append(
                            product.get('feedbacks', NOT_FOUND_NUMBER)
                        )
                        results['Рейтинг'].append(
                            product.get('rating', NOT_FOUND_NUMBER)
                        )
            except requests.exceptions.HTTPError:
                logging.warning(
                    'Проблемы с получением данных, '
                    f'артикул {vendor_code}')
            except AttributeError as e:
                logging.error(
                    'Ошибка при обработке данных '
                    f'для артикула {vendor_code}: {e}'
                )
        xlsx_writer(results)
    else:
        logging.critical('Ошибка загрузки данных!')


if __name__ == "__main__":
    parse_product()
