import refinitiv.dataplatform.eikon as ek
from params import usdrub_tod, usdrub_tom, start_date, fx_columns, ek_colname, rics, EIKON_API_KEY

ek.set_app_key(EIKON_API_KEY)

# 1. get_eikon_data возвращает датафрейм, где даты - это строки, важно это учесть,
# в том числе при загрузке в БД
# 2. Айкон возвращает данные, где пропуски заполнены <NA> - надо это учесть в самой функции,
# исправить на замену на None
# 3. Надо обязательно сравнить те столбцы, которые я смог найти в айконе,
# и те, которые прописал в schema
# 4. df.replace(np.nan, None)
# 5. df.to_sql
