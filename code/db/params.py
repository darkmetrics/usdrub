# этот файл предназначен для хранения параметров, связанных с БД и загрузкой данных
import os

# получим логин и пароль для PostgreSQL из переменных окружения Windows
PSQL_USER = os.environ.get('PSQL_USER')
PSQL_PASSWORD = os.environ.get('PSQL_PASSWORD')
# получение ключа API для Eikon
# ВАЖНО: этот ключ связан с аккаунтом ВШЭ, логин аккаунта: student3@hse.ru
EIKON_API_KEY = os.environ.get('EIKON_API_KEY')

db_name = 'daily'
# переход на плавающий курс: 10-11-2014 https://tass.ru/ekonomika/1562762
start_date = '2014-10-01'

# список тикеров для нужных переменных в системе Thomson Reuters
rics = [  # курс евро
    'EUR=',
    # доходности государственных облигаций
    'US10YT=RR', 'DE10YT=RR', 'RU10YT=RR', 'US5YT=RR', 'DE5YT=RR', 'RU5YT=RR',
    # сырье: нефть, газ, золото
    'LCOc1', 'XAU='
]

usdrub_tod = "USD000000TOD"
usdrub_tom = "USD000UTSTOM"
# столбцы данных для запроса к API ММВБ
fx_columns = ['TRADEDATE', 'CLOSE', 'VOLRUR']
# и для запроса к Thomson Reuters Eikon API
ek_colname = 'CLOSE'
