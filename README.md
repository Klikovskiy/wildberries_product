# Парсинг данных с карточки товара Wildberries

Сбор данных осуществляется через GET запрос к API Wildberries, в качестве параметра передается Артикул товара на Маркетплейсе.

## Как работать с проектом
         
1. Клонируйте репозиторий и перейдите корневую директорию:
```      
git clone https://github.com/klikovskiy/wildberries_product
cd wildberries_product
```    
2. Установите зависимости проекта.
```      
pip install -r requirements.txt
```   
3. Создайте файл task_parsing.txt. Поместите туда артикулы товаров, каждый с новой строки, пример ниже.
```
12345612
65432121
09876512
```
4. Запустите скрипт parsing_wb.py
5. Если все сделано правильно, увидите лог выполнения.
```
2023-03-30 01:00:00,00, INFO, root, Выполняю поиск данных по артикулу: 12345612.
2023-03-30 01:00:00,00, INFO, root, Выполняю поиск данных по артикулу: 65432121.
2023-03-30 01:00:00,00, INFO, root, Выполняю поиск данных по артикулу: 09876512.
```

_В скрипте учтена обработка часто возникающих ошибок. 
Ведется логирование действий в файл work_logs.log.
При желании, можно включить более подробное логирование 
в параметре ```level=logging.INFO```, переключив на ```level=logging.DEBUG```_



## Требования к проекту
- Python 3.0+

_Проект размещен в ознакомительных целях. 
Не провожу консультации, как его запустить или что-то дополнить/поменять!_