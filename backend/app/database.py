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

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# SQLALCHEMY_DATABASE_URL = f"mysql+psycopg2://{username}:{password}@{host}:{port}/{DB_NAME}"

engine = create_engine(os.getenv("DATABASE_URL"), pool_size=11120, max_overflow=0)


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
