import requests
import json
from datetime import datetime, date
from params import usdrub_tod, usdrub_tom, start_date, fx_columns

current_date = datetime.now()


# функция для загрузки котировок валютных курсов с ММВБ
def get_fx(ticker: str,
           start_date: str,
           end_date: str,
           columns: list,
           boargroups: int = 13,
           format: str = 'json'
           ) -> dict:
    """
    Скачивает историю котировок валютных курсов по IMOEX API.
    
    Аргументы
    ----------
    ticker:str. Тикер валютной пары в системе ММВБ
    start_date:str. Начальная дата для запрашиваемых данных.
    end_date:str. Конечная дата для запрашиваемых данных
    columns:list. Список строковых имен столбцов, которые нас интересуют.
        Возможные значения для валют: "BOARDID", "TRADEDATE", "SHORTNAME",
        "SECID", "OPEN", "LOW", "HIGH", "CLOSE", "NUMTRADES", "VOLRUR", "WAPRICE"
    boargroups:int, default=13. Номер группы режима торгов. 13 - безадресные
        системные сделки, то, что нас интересует в данном случае.
    format:str, default='json'. В каком формате запрос вернет данные. Возможные
        значения: 'json', 'xml, 'html'.
    
    Additional notes:
    -----------------
    Чтобы выкачать нужные данные по ISS API, надо:
    1. изучить developer guide
    2. двигаться по url по узлам, каждый раз изучая содержимое узла с помощью index.json.
    Начать можно с удобной стартовой ссылки, в которой есть все основные рынки и режимы 
    торгов: http://iss.moex.com/iss/index.json
    """

    print(f'Скачиваю данные с ММВБ для {ticker}...')
    colstring = ','.join(columns)
    data = []
    start = 0
    while True:
        query = (f'http://iss.moex.com/iss/history/engines/currency/markets/selt/'
                 f'boardgroups/{boargroups}/securities/{ticker}.{format}?'
                 f'from={start_date}&till={end_date}&start={start}&history.columns={colstring}')

        resp = requests.get(query)
        resp = json.loads(resp.text)
        data += resp['history']['data']
        # в ответе есть специальный курсор, он показывает, сколько наблюдений
        # всего вернет запрос и сколько мы уже получили
        cursor = dict(zip(resp['history.cursor']['columns'],
                          resp['history.cursor']['data'][0]))
        # сравним полученное число наблюдений с максимальным
        if cursor['TOTAL'] < cursor['INDEX'] + cursor['PAGESIZE']:
            return {'columns': columns, 'values': data}
        # максимальное количество наблюдений за 1 запрос к API=100
        start += 100


out = get_fx(ticker=usdrub_tom,
             start_date=start_date,
             end_date=current_date.strftime("%Y-%m-%d"),
             columns=fx_columns)
print(out)
