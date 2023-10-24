from atexit import register

from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Настройки подключения к базе данных
PG_DB = "app"
PG_USER = "app"
PG_PASSWORD = "1234"
PG_HOST = "127.0.0.1"
PG_PORT = 5431
PG_DNS = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"

engine = create_engine(PG_DNS)    # Подключение к базе по заданному URL-базы (DNS)

register(engine.dispose)     # По окончании работы приложения наша БД должна отключиться

Session = sessionmaker(bind=engine)
Base = declarative_base(bind=engine)


class Advertisement(Base):
    """ Модель объявлений """
    __tablename__ = "app_adverts"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, index=True)
    description = Column(String)
    creation_time = Column(DateTime, server_default=func.now())
    owner = Column(String, nullable=False)


print("\n  База данных подключена...")    # BaseEmulator
# Выполняет миграции, подключается к базе данных
Base.metadata.create_all()
