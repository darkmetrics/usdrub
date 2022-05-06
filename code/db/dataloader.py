import json
import requests
import investpy
import pandas as pd
import yfinance as yf
import refinitiv.dataplatform.eikon as ek
from datetime import datetime
from functools import reduce
from typing import Union
from investpy.bonds import get_bond_historical_data


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
           fillna_method: Union[str, None] = None
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
            if fillna_method:
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
                   fillna_method: Union[bool, str] = None
                   ) -> pd.DataFrame:
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
    fillna_method: bool or str, default 'ffill'. Как заполнить пропуски (из pandas fillna).
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


def get_investing_bonds_data(tickers: list,
                             start_date: str,
                             end_date: str,
                             fillna: Union[bool, str] = None,
                             dropna: bool = True,
                             indicator: str = 'Close') -> pd.DataFrame:
    """
    Скачивает данные с Investing.com.

    Параметры:
    ----------
    tickers: list.
        Словарь с названием (иями) тикера (тикеров
    start_date:
        Дата начала набора данных для заданных тикеров.
    end_date:
        Последняя дата, на которую надо скачать историю для заданных тикеров.
    fillna: str, default None.
        Как заполнять пропущенные значения.
    dropna: bool, default None.
        Удалять ли строки, в которых отсутствуют все значения.
    indicator: str, default Close.
    """
    start_date = "/".join(reversed(start_date.split('-')))
    end_date = "/".join(reversed(end_date.split('-')))
    print(start_date)
    df_list = []
    for t in tickers:
        print(f"Скачиваю данные для тикера {t}...")
        try:
            df_list.append(get_bond_historical_data(bond=t,
                                                    from_date=start_date,
                                                    to_date=end_date))
        except Exception as e:
            print(f"Загрузка не удалась. Описание ошибки: {e}")

    data = pd.concat([x['Close'] for x in df_list],
                     join='outer',
                     axis=1)
    data.columns = tickers
    if fillna:
        data.fillna(method=fillna, inplace=True)
    if dropna:
        data.dropna(inplace=True)
    return data


def get_bond_names(country_dict: dict) -> Union[str, dict]:
    """
    Ищет названия тикеров гособлигаций в библиотеке investpy

    Параметры:
    ----------
    country_dict: dict.
        Словарь с параметрами поиска. Ключ - название страны, значение -
        список сроков до погашения государственных облигаций заданной страны.
        Пример:
        {'russia': [5, 10],
         'united states': [5, 10]}
    """
    name_dict = {x.lower(): {} for x in country_dict.keys()}
    for country, maturities in country_dict.items():
        country = country.lower()
        # получим список названий бондов для страны
        # обработчик ошибок для неверных названий стран уже есть в investpy
        bond_list = investpy.bonds.get_bonds(country)
        for m in maturities:
            name = bond_list['name'][bond_list['name'].str.contains(str(m),
                                                                    regex=False)].values[0]
            name_dict[country][m] = name
    return name_dict


def get_yf_data(tickers: Union[str, list],
                start_date: str,
                end_date: str
                ) -> Union[pd.Series, pd.DataFrame]:
    """
    Скачивает исторические котировки фьючерсов на сырье с помощью API
    yahoo.finance (библиотека yfinance).

    Параметры:
    ----------
    tickers: str or list.
        Тикер или список тикеров.
    start_date:
        Дата начала датасета, который хотим получить.
    end_date:
        Последняя дата, на которую хотим получить данные.
    """
    for ticker in tickers:
        print(f"Скачиваю данные для тикера {ticker}")
    df = yf.download(tickers=tickers,
                     start=start_date,
                     end=end_date)
    df = df['Close']
    df.index.name = 'date'
    return df


# полезные ссылки
# https://investpy.readthedocs.io/_api/commodities.html
# https://investpy.readthedocs.io/_api/bonds.html

if __name__ == '__main__':
    from params import yf_tickers

    out = get_bond_names(country_dict={'RUSSIA': [5, 10],
                                       'UNITED STATES': [5, 10],
                                       'GERMANY': [5, 10]})
    print(out)
    out['germany'][5] = 'Germany 5Y'
    tickers = [x for y in out.values() for x in y.values()]
    print(tickers)
    data = get_investing_bonds_data(tickers,
                                    start_date='2022-01-01',
                                    end_date='2022-10-04',
                                    dropna=False)
    print(data)
    print(data.isna().sum())
    coms = get_yf_data(tickers=yf_tickers,
                       start_date='2022-01-01',
                       end_date='2022-10-04'
                       )
    print(coms)
    print(coms.isna().sum())
