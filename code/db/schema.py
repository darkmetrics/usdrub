from sqlalchemy import Column, BigInteger, Date, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# создадим схему табличек для базы данных

class Daily(Base):
    __tablename__ = 'daily'
    """табличка для хранения дневных котировок"""
    # первичный ключ - дата
    date = Column(Date, primary_key=True)
    # валюты
    usdrub_tod = Column(Float)
    usdrub_tom = Column(Float)
    eurusd = Column(Float)
    # доходности государственных облигаций
    ust10 = Column(Float)
    ger10 = Column(Float)
    ofz10 = Column(Float)
    ust5 = Column(Float)
    ger5 = Column(Float)
    ofz5 = Column(Float)
    # сырье
    brent = Column(Float)
    # urals = Column(Float)
    gas = Column(Float)
    gold = Column(Float)
    # российский фондовый индекс
    imoex = Column(Float)



class Volume(Base):
    __tablename__ = 'volumes'
    """табличка для хранения объемов"""
    date = Column(Date, primary_key=True)
    usdrub_tod = Column(BigInteger)
    usdrub_tom = Column(BigInteger)
