import json
import requests
import pandas as pd
import refinitiv.dataplatform.eikon as ek
from datetime import datetime
from functools import reduce


# from params import usdrub_tod, usdrub_tom, start_date


def flatten(keys: list,
            values: list) -> list:
    """
    Возвращает массив, развернутый в список словарей, где
    ключи - имена столбцов, значения - данные из списка списков
    """
    return [{k: v[i] for i, k in enumerate(keys)} for v in values]


# функция для загрузки котировок валютных курсов с ММВБ
def get_fx(ticker: str,
           start_date: str,
           end_date: str,
           columns: list,
           boargroups: int = 13,
           format: str = 'json',
           fillna_method: str = 'ffill'
           ) -> pd.DataFrame:
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
    fillna_method:str, default='ffill'. Как заполнять пропуски в табличках (
        см pandas fillna).
    
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
    short_name = f'{ticker[:3]}RUB{ticker[-3:]}'
    data = []
    start = 0
    while True:
        query = (f'http://iss.moex.com/iss/history/engines/currency/markets/selt/'
                 f'boardgroups/{boargroups}/securities/{ticker}.{format}?'
                 f'from={start_date}&till={end_date}&start={start}&history.columns={colstring}')

        r = requests.get(query)
        r = json.loads(r.text)
        data += r['history']['data']
        # в ответе есть специальный курсор, он показывает, сколько наблюдений
        # всего вернет запрос и сколько мы уже получили
        cursor = dict(zip(r['history.cursor']['columns'],
                          r['history.cursor']['data'][0]))
        # сравним полученное число наблюдений с максимальным
        if cursor['TOTAL'] < cursor['INDEX'] + cursor['PAGESIZE']:
            data = flatten(keys=r['history']['columns'], values=data)

            # переделаем в Pandas DataFrame
            df = pd.DataFrame(data)
            df.columns = ['date', f'{short_name}', 'volume']
            # преобразуем строковые даты в datetime и оставим только дату
            df['date'] = pd.to_datetime(df['date'])
            df['date'] = df['date'].dt.date
            df.index = df['date']
            df.index.name = 'date'
            df.drop(columns='date', inplace=True)
            # посчитаем объем в долларах
            df['volume'] = df['volume'].div(df[f'{short_name}'])
            # заполним пропуски
            df.fillna(method=fillna_method, inplace=True)
            # удалим первые несколько наблюдений, если в них пропуски
            df.dropna(inplace=True)
            return df

        # максимальное количество наблюдений за 1 запрос к API=100
        start += 100


def get_eikon_data(rics: list,
                   start_date: str,
                   end_date: str,
                   colname: str = 'CLOSE',
                   fillna_method: str = 'ffill') -> pd.DataFrame:
    """
    Выкачивает данные из Thomson Reuters Eikon по списку тикеров.
    Возвращает pandas DataFrame с заданным столбцом для каждого тикера и датами.

    Параметры:
    ----------
    rics: list. Список интересующих нас тикеров в системе Thomson Reuters.
    start_date: str. Начальная дата для запрашиваемых данных.
    end_date: str. Начальная дата для запрашиваемых данных.
    colname:str. Имя столбца, который мы вернем из таблички, загруженной через
        Eikon. Нас интересует цена закрытия инструмента - CLOSE
    fillna_method:str, default 'ffill'. Как заполнить пропуски (из pandas fillna).
    """
    # получим данные циклом, потом переписать на асинхоронный вариант
    dfs = []
    for ric in rics:
        # не забыть переименовать столбцы и выбрать close
        print(f'Скачиваю данные из Thomson Reuters Eikon для {ric}...')
        df = ek.get_timeseries(rics=ric,
                               start_date=start_date,
                               end_date=end_date)

        df.rename(columns={colname: ric}, inplace=True)
        dfs.append(df[ric])

    data = reduce(lambda x, y: pd.merge(x, y,
                                        how='outer',
                                        left_index=True,
                                        right_index=True),
                  dfs)

    data['date'] = data.index
    data.index = data['date'].dt.date
    data.index.name = 'date'
    data.drop(columns='date', inplace=True)
    # заполним пропуски
    data.fillna(method=fillna_method, inplace=True)
    # удалим первые несколько наблюдений, если в них пропуски
    data.dropna(inplace=True)
    return data


if __name__ == '__main__':
    # out = get_fx(ticker=usdrub_tom,
    #              start_date=start_date,
    #              end_date=current_date.strftime("%Y-%m-%d"),
    #              columns=fx_columns)
    # print(out)
    # from params import rics

    # out = get_eikon_data(rics=rics,
    #                      start_date=start_date,
    #                      end_date=current_date.strftime("%Y-%m-%d"),
    #                      colname=ek_colname)
    pass
