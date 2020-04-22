import os

import sqlalchemy
import sqlalchemy.ext.declarative as dec
from sqlalchemy import orm

SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception('Необходимо указать файл базы данных.')

    conn_str_sqlite = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    conn_str = os.environ.get('DATABASE_URL', conn_str_sqlite)
    print(f'Подключение к базе данных по адресу {conn_str}')

    engine = sqlalchemy.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> orm.Session:
    global __factory
    return __factory()
