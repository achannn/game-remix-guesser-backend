import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError, StatementError, DatabaseError
from sqlalchemy.orm.query import Query as _Query
from time import sleep
from . import internal

username=""
password = ""
host = ""
port = ""
DB_NAME = ""

if os.getenv('ENV') == "DEV":
    internal.log_info("environment is dev")
    username=os.getenv('MYSQL_USER')
    password = os.getenv('MYSQL_ROOT_PASSWORD')
    host = os.getenv('MYSQL_HOST')
    port = os.getenv('MYSQL_PORT')
    DB_NAME = os.getenv('MYSQL_DATABASE')


SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{DB_NAME}"
internal.log_info(username)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'auth_plugin': 'mysql_native_password'}
)


class RetryingQuery(_Query):
    __max_retry_count__ = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __iter__(self):
        attempts = 0
        while True:
            attempts += 1
            try:
                return super().__iter__()
            except OperationalError as ex:
                if "server closed the connection unexpectedly" not in str(ex):
                    raise
                if attempts <= self.__max_retry_count__:
                    sleep_for = 2 ** (attempts - 1)
                    internal.log_error(
                        "/!\ Database connection error: retrying Strategy => sleeping for {}s"
                    " and will retry (attempt #{} of {}) \n Detailed query impacted: {}".format(
                        sleep_for, attempts, self.__max_retry_count__, ex)
                )
                    sleep(sleep_for)
                    continue
                else:
                    raise
            except StatementError as ex:
                if "reconnect until invalid transaction is rolled back" not in str(ex):
                    raise
                self.session.rollback()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()
