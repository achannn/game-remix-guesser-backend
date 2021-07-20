import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

username = os.getenv('MYSQL_USER')
password = os.getenv('MYSQL_ROOT_PASSWORD')
host = os.getenv('MYSQL_HOST')
port = os.getenv('MYSQL_PORT')
DB_NAME = os.getenv('MYSQL_DB')

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{username}:{password}@{host}:{port}"

db = SQLAlchemy(app)

@app.route('/')
def hello_world():
  return 'Hello, Docker!'
