import pandas as pd
from datetime import datetime
import refinitiv.dataplatform.eikon as ek

from db import Db
from schema import Base
from dataloader import get_fx, get_eikon_data
from params import EIKON_API_KEY, usdrub_tod, usdrub_tom, start_date, fx_columns, ek_colname, rics, \
    PSQL_USER, PSQL_PASSWORD, db_name

# залогинимся в терминале Eikon
ek.set_app_key(EIKON_API_KEY)
# будем выгружать котировки вплоть до сегодняшней даты
current_date = datetime.now()

# выкачаем курсы рубля и объемы с ММВБ
fx_kwargs = {'start_date': start_date,
             'end_date': current_date.strftime("%Y-%m-%d"),
             'columns': fx_columns,
             'fillna_method': 'ffill'}

tod = get_fx(ticker=usdrub_tod, **fx_kwargs)
tom = get_fx(ticker=usdrub_tom, **fx_kwargs)

# объединим в единые таблички данные по валютам и их объемам
fx = pd.merge(tod.drop(columns='volume'), tom.drop(columns='volume'),
              how='outer', left_index=True, right_index=True)
volumes = pd.merge(tod['volume'], tom['volume'],
                   how='outer', left_index=True, right_index=True)
# переименуем 'volume' в названия тикеров для объемов
volumes.columns = fx.columns

# выкачаем данные из Eikon
tr = get_eikon_data(rics=rics,
                    start_date=start_date,
                    end_date=current_date.strftime("%Y-%m-%d"),
                    colname=ek_colname,
                    fillna_method='ffill')
# объединим все данные в единый датафрейм
daily = pd.merge(fx, tr, how='outer', left_index=True, right_index=True)
# разберемся с пропусками в объединенном датафрейме
daily.fillna(method='ffill', inplace=True)
daily.dropna(inplace=True)

# подсоединимся к БД, контекстный менеджер закроет соедениние с БД автоматически
with Db(db_name, PSQL_USER, PSQL_PASSWORD, Base) as db:
    # удалим все наблюдения из всех табличек
    db.clear_data()
    # загрузим данные в таблички
    db.load('daily', daily)
    db.load('volumes', volumes)

# 1. get_eikon_data возвращает датафрейм, где даты - это строки, важно это учесть,
# в том числе при загрузке в БД
# 2. Надо обязательно сравнить те столбцы, которые я смог найти в айконе,
# и те, которые прописал в schema
