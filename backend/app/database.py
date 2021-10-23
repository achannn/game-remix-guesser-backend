import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError, StatementError, DatabaseError
from sqlalchemy.orm.query import Query as _Query
from time import sleep
from . import internal


# response = client.access_secret_version(request={"name": 'projects/723869654657/secrets/MYSQL_USER/versions/1'})

def access_secret_version(project_id, secret_id, version_id):
    """
    Access the payload for the given secret version if one exists. The version
    can be a version number as a string (e.g. "5") or an alias (e.g. "latest").
    """

    # Import the Secret Manager client library.
    from google.cloud import secretmanager

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    # Access the secret version.
    response = client.access_secret_version(request={"name": name})

    # WARNING: Do not print the secret in a production environment - this
    # snippet is showing how to access the secret material.
    return response.payload.data.decode("UTF-8")

username=""
password = ""
host = ""
port = ""
DB_NAME = ""

if os.getenv('ENV') == "DEV":
    print("environment is dev")
    username=os.getenv('MYSQL_USER')
    password = os.getenv('MYSQL_ROOT_PASSWORD')
    host = os.getenv('MYSQL_HOST')
    port = os.getenv('MYSQL_PORT')
    DB_NAME = os.getenv('MYSQL_DATABASE')
else:
    PROJECT_ID = "723869654657"

    username=access_secret_version(project_id=PROJECT_ID, secret_id="MYSQL_USER", version_id=1)
    password =access_secret_version(project_id=PROJECT_ID, secret_id="MYSQL_PASSWORD", version_id=1)
    host =access_secret_version(project_id=PROJECT_ID, secret_id="MYSQL_HOST", version_id=1)
    port =access_secret_version(project_id=PROJECT_ID, secret_id="MYSQL_PORT", version_id=1)
    DB_NAME =access_secret_version(project_id=PROJECT_ID, secret_id="MYSQL_DATABASE", version_id=2)


# def access_secret_version(project_id, secret_id, version_id):
#     """
#     Access the payload for the given secret version if one exists. The version
#     can be a version number as a string (e.g. "5") or an alias (e.g. "latest").
#     """

#     # Import the Secret Manager client library.
#     from google.cloud import secretmanager

#     # Create the Secret Manager client.
#     client = secretmanager.SecretManagerServiceClient()

#     # Build the resource name of the secret version.
#     name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

#     # Access the secret version.
#     response = client.access_secret_version(request={"name": name})

#     # Print the secret payload.
#     #
#     # WARNING: Do not print the secret in a production environment - this
#     # snippet is showing how to access the secret material.
#     payload = response.payload.data.decode("UTF-8")
#     print("Plaintext: {}".format(payload))


SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{DB_NAME}"
print(username)

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
