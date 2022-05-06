# этот файл предназначен для хранения параметров, связанных с БД и загрузкой данных
import os

# получим логин и пароль для PostgreSQL из переменных окружения Windows
PSQL_USER = os.environ.get('POSTGRES_USER')
PSQL_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
# получение ключа API для Eikon
# ВАЖНО: этот ключ связан с аккаунтом ВШЭ, логин аккаунта: student3@hse.ru
# EIKON_API_KEY = os.environ.get('EIKON_API_KEY')

# теперь у нас новая БД, с данными из бесплатных источников
# db_name = 'usdrub'
db_name = 'yahoo'
# переход на плавающий курс: 10-11-2014 https://tass.ru/ekonomika/1562762
start_date = '2014-10-01'

# список тикеров для нужных переменных в системе Thomson Reuters
rics = [  # курс евро
    'EUR=',
    # доходности государственных облигаций
    'US10YT=RR', 'DE10YT=RR', 'RU10YT=RR', 'US5YT=RR', 'DE5YT=RR', 'RU5YT=RR',
    # сырье: нефть, газ, золото
    # с фьючерсом на газ надо разобраться, взял пока Dutch TTF Gas Futures
    'LCOc1', 'TRNLTTFMc1', 'XAU='
]

usdrub_tod = "USD000000TOD"
usdrub_tom = "USD000UTSTOM"
# столбцы данных для запроса к API ММВБ
fx_columns = ['TRADEDATE', 'CLOSE', 'VOLRUR']
# и для запроса к Thomson Reuters Eikon API
ek_colname = 'CLOSE'

# в связи с прекращением работы Eikon в РФ,
# будем использовать бесплатные некачественные данные.
# Да здравствуют модели на никчемных данных!

# названия стран и сроки до погашения облигаций
# для загрузки YTM суверенных бондов с investing.com
bond_dict = {'russia': [5, 10],
             'united states': [5, 10],
             'germany': [5, 10]}
# курс евро, тикеры сырьевых фьючерсов (нефть, газ, золото) и IMOEX
# для загрузки с Yahoo.Finance
yf_tickers = ['EURUSD=X', 'BZ=F', 'TTF=F', 'GC=F', 'IMOEX.ME']

# соответствие тикеров на ММВБ, Yahoo и Investing названиям столбцов в БД
# ключи расположены именно в том порядке, в каком хранятся столбцы в таблице daily
mapping_dict = {
    'usdrub_tod':"USDRUBTOD",
    'usdrub_tom':"USDRUBTOM",
    'eurusd':'EURUSD=X',
    'ust10':"U.S. 10Y",
    'ger10':"Germany 10Y",
    'ofz10':"Russia 10Y",
    'ust5':"U.S. 5Y",
    'ger5':"Germany 5Y",
    'ofz5':"Russia 5Y",
    'brent':"BZ=F",
    'gas':"TTF=F",
    'gold':"GC=F",
    'imoex':"IMOEX.ME"
}
