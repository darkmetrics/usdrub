from sqlalchemy import create_engine, MetaData, Table, Column, BigInteger, Date, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database

from schema import Base

import pandas as pd
import psycopg2

from params import psql_user, psql_pass

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
        # если БД существует, подключимся
        if database_exists(self.engine.url):
            print('database already exists')
            Session = sessionmaker(bind=self.engine)
            session = Session()
            self.session = session
        # иначе создадим, прогрузив схему
        else:
            print('creating database...')
            self.create()

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

    def drop(self):
        """Удаляет БД, если она уже существует"""
        pass

    def get_df(self, name: str):
        """Возвращает таблицу из БД в формате Pandas DataFrame"""
        pass


with Db('somename', psql_user, psql_pass, base=Base) as db:
    pass
