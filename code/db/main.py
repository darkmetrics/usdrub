import pandas as pd
from datetime import datetime
import refinitiv.dataplatform.eikon as ek

from db import Db
from schema import Base
from dataloader import get_fx, get_bond_names, get_investing_bonds_data, get_yf_data
from params import usdrub_tod, usdrub_tom, start_date, fx_columns, \
    yf_tickers, bond_dict, mapping_dict, \
    PSQL_USER, PSQL_PASSWORD, db_name

# залогинимся в терминале Eikon
# ek.set_app_key(EIKON_API_KEY)
# будем выгружать котировки вплоть до сегодняшней даты
current_date = datetime.now()

# выкачаем курсы рубля и объемы с ММВБ
fx_kwargs = {'start_date': start_date,
             'end_date': current_date.strftime("%Y-%m-%d"),
             'columns': fx_columns,
             'fillna_method': None}

tod = get_fx(ticker=usdrub_tod, **fx_kwargs)
tom = get_fx(ticker=usdrub_tom, **fx_kwargs)

# объединим в единые таблички данные по валютам и их объемам
fx = pd.merge(tod.drop(columns='volume'), tom.drop(columns='volume'),
              how='outer', left_index=True, right_index=True)
volumes = pd.merge(tod['volume'], tom['volume'],
                   how='outer', left_index=True, right_index=True)
print(volumes)
# переименуем 'volume' в названия тикеров для объемов
volumes.columns = fx.columns
print(fx)

# выкачаем данные из Eikon
# с марта 2022 года это невозможно из-за санкций
# tr = get_eikon_data(rics=rics,
#                     start_date=start_date,
#                     end_date=current_date.strftime("%Y-%m-%d"),
#                     colname=ek_colname,
#                     fillna_method='ffill')

# получим коды государственных облигаций с сайта Investing.com
bond_names = get_bond_names(bond_dict)
# косая библиотека investpy, для одного бонда названия грузится неверно
bond_names['germany'][5] = 'Germany 5Y'
bond_tickers = [x for y in bond_names.values() for x in y.values()]
# выгрузим доходности к погашению государственных облигаций
bonds = get_investing_bonds_data(bond_tickers,
                                 start_date=start_date,
                                 end_date=current_date.strftime("%Y-%m-%d"),
                                 dropna=False)

# выгрузим исторические котировки фьючерсов на сырьe, курс евро и индекс IMOEX
# с сайта Yahoo.Finance!
yf_data = get_yf_data(tickers=yf_tickers,
                      start_date=start_date,
                      end_date=current_date.strftime("%Y-%m-%d")
                      )

# объединим все данные в единый датафрейм
daily = pd.concat((fx, bonds, yf_data),
                  ignore_index=False,
                  axis=1)
# переупорядочим столбцы так, как они будут храниться в БД
daily = daily[list(mapping_dict.values())]
# переименуем столбцы так, как они зовутся в базе данных
# хотя это и не обязательно
daily.rename(columns=dict(zip(list(mapping_dict.values()),
                              list(mapping_dict.keys()))),
             inplace=True)
print(daily)
daily.index.name = 'date'

# daily = pd.merge(fx, tr, how='outer', left_index=True, right_index=True)
# разберемся с пропусками в объединенном датафрейме
# daily.fillna(method='ffill', inplace=True)
# daily.dropna(inplace=True)
# не будем спешить с пропусками
# заполним лишь пропуски для регрессоров, курс рубля трогать не будем
# потому что в марте 2022 торгов не было,
# но потенциально нам было бы интересно оценить пропущенные значения

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
