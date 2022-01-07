db_name = 'quotes'
# переход на плавающий курс: 10-11-2014 https://tass.ru/ekonomika/1562762
start_date = '2014-10-01'
rics = []
usdrub_tod = "USD000000TOD"
usdrub_tom = "USD000UTSTOM"
# столбцы данных для запроса к API ММВБ
fx_columns = ['TRADEDATE', 'CLOSE', 'VOLRUR']
