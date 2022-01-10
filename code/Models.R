library(dplyr) # работа с табличками
library(ggplot2) # графики
library(GGally)
library(DBI) # подключение к Postgres



#|---------------------------
#|  Загрузка данных из БД  --
#|---------------------------

# загрузим переменны окружения с логином и паролем для Postgres
PSQL_USER <- Sys.getenv('POSTGRES_USER')
PSQL_PASSWORD <- Sys.getenv('POSTGRES_PASSWORD')

# соединимся с БД
con <- dbConnect(RPostgres::Postgres(),dbname = 'usdrub', 
                 host = 'localhost', 
                 port = 5432, 
                 user = PSQL_USER,
                 password = PSQL_PASSWORD)

# выгрузим дневные данные
t <- data.frame(dbReadTable(con, 'daily'))
glimpse(t)


#|--------------------------
#|  Предобработка данных  --
#|--------------------------

fx <- data.frame(t)
# проверим что копия не зависит от исходной выгрузки
stopifnot(tracemem(fx)!=tracemem(t))

# удалим usdrubtod, как менее ликвидный
fx <- subset(fx, select = -c(usdrub_tod))

# посчитаем спреды доходностей гособлигаций
fx['us10_spread'] <- fx['ofz10']-fx['ust10']
fx['ge10_spread'] <- fx['ofz10']-fx['ger10']
fx['us5_spread'] <- fx['ofz5']-fx['ust5']
fx['ge5_spread'] <- fx['ofz5']-fx['ger5']

# удалим сами доходности гособлигаций
fx <- subset(fx, select = -c(ust10, ger10, ofz10, ust5, ger5, ofz5))
glimpse(fx)

# TODO
# нарисуем графики переменных в зависимости от времени


# нарисуем ggpairs, выкинем дату
pairtitle <- "Распределения переменных
до (красные) и во время пандемии"

ggpairs(subset(fx, select=-c(date)),
        # графики на нижней диагонали
        lower = list(combo = wrap("facethist", 
                                       alpha = 0.3, 
                                       size=0.2)),
        # цвета 
        aes(color=
              as.integer(format(as.Date(fx$date), format='%Y')) >= 2019),
        # графики на диагонали
        diag = list(continuous = wrap("densityDiag", alpha = 0.5)),
        title=pairtitle
        ) +
  # форматирование боксов с корреляцией
  theme(legend.position = "none", 
        panel.grid.major = element_blank(), 
        axis.ticks = element_blank(), 
        panel.border = element_rect(linetype = "dashed", 
                                    colour = "black", 
                                    fill = NA))
