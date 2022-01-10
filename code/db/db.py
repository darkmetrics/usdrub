import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from schema import Base
from params import db_name, PSQL_USER, PSQL_PASSWORD


# сам класс для работы с БД

class Db:
    def __init__(self, name: str, user: str, password: str, base):
        """
        :param name:
        :param user:
        :param password:
        :param base:
        """
        self.name = name
        self.session = None
        self.engine = None
        self.user = user
        self.password = password
        self.conn_string = f"postgresql+psycopg2://{user}:{password}@localhost/{self.name}"
        self.base = base

    def __enter__(self):
        """Подключение к БД через контекстный менеджер"""
        self.engine = create_engine(self.conn_string)
        # если БД не существует, создадим, прогрузив схему
        if not database_exists(self.engine.url):
            print('База данных не существует, создаю ее по схеме из schema.py...')
            self.create()
        # подключимся
        Session = sessionmaker(bind=self.engine)
        session = Session()
        self.session = session

    def create(self):
        """Создает БД на основе схемы"""
        create_database(self.engine.url)
        self.base.metadata.create_all(self.engine)

    def __exit__(self, exception_type, exception_val, trace):
        """Предназначен для закрытия всех соединений в БД"""
        try:
            self.session.close()
        # если соединение не устанавливалось, то и сессии нет
        except AttributeError as e:
            pass
        finally:
            self.engine.dispose()

    def clear_data(self):
        """Удаляет записи из всех таблиц в БД"""
        for table in reversed(self.base.metadata.sorted_tables):
            print(f'Удаляю данные из таблицы {table}...')
            self.session.execute(table.delete())
        self.session.commit()

    def load(self, name: str, data: pd.DataFrame):
        """
        Загружает данные в таблицу

        Параметры:
        ----------
        name: str, имя таблицы
        data: pandas DataFrame, данные, которые хотим загрузить.
            Данные должны быть уже предобработаны для загрузки в Postgres.
        """
        print(f'Загружаю данные в таблицу {name}...')
        data.to_sql(name, self.engine)

    def drop(self):
        """Удаляет БД, если она уже существует"""
        pass

    def get_df(self, name: str):
        """Возвращает таблицу name из БД в формате Pandas DataFrame"""
        return pd.read_sql(self.session.query(name), self.session.bind)


with Db(db_name, PSQL_USER, PSQL_PASSWORD, base=Base) as db:
    pass
