"""Setup at app startup"""
import os
import sqlalchemy
from flask import Flask
from yaml import load, Loader
import io
from flask_mysqldb import MySQL


def init_connection_engine():
    """ initialize database setup
    Takes in os variables from environment if on GCP
    Reads in local variables that will be ignored in public repository.
    Returns:
        pool -- a connection to GCP MySQL
    """


    # detect env local or gcp
    if os.environ.get('GAE_ENV') != 'standard':
        try:
            variables = load(open("app.yaml"), Loader=Loader)
        except OSError as e:
            print("Make sure you have the app.yaml file setup")
            os.exit()

        env_variables = variables['env_variables']
        for var in env_variables:
            os.environ[var] = env_variables[var]

    pool = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL(
            drivername="mysql+pymysql",
            username=os.environ.get('MYSQL_USER'),
            password=os.environ.get('MYSQL_PASSWORD'),
            database=os.environ.get('MYSQL_DB'),
            host=os.environ.get('MYSQL_HOST')
        )
    )

    return pool


app = Flask(__name__)

app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')

db = init_connection_engine()

mysql = MySQL(app)


def gen_map():
  team_str = "Michigan 0\nBaylor 1\nIllinois 2\nGonzaga 3\nIowa 4\nOhio St. 5\nHouston 6\nAlabama 7\nWest Virginia 8\nTexas 9\nKansas 10\nArkansas 11\nFlorida St. 12\nVirginia 13\nPurdue 14\nOklahoma St. 15\nVillanova 16\nTennessee 17\nCreighton 18\nColorado 19\nTexas Tech 20\nBYU 21\nUSC 22\nSan Diego St. 23\nFlorida 24\nConnecticut 25\nClemson 26\nOregon 27\nOklahoma 28\nNorth Carolina 29\nLSU 30\nLoyola Chicago 31\nSt. Bonaventure 32\nMissouri 33\nWisconsin 34\nGeorgia Tech 35\nRutgers 36\nVirginia Tech 37\nMaryland 38\nVCU 39\nMichigan St. 40\nWichita St. 41\nSyracuse 42\nUCLA 43\nUtah St. 44\nDrake 45\nGeorgetown 46\nOregon St. 47\nUC Santa Barbara 48\nWinthrop 49\nOhio 50\nNorth Texas 51\nUNC Greensboro 52\nLiberty 53\nColgate 54\nEastern Washington 55\nAbilene Christian 56\nMorehead St. 57\nIona 58\nOral Roberts 59\nGrand Canyon 60\nCleveland St. 61\nDrexel 62\nMount St. Mary's 63\nHartford 64\nNorfolk St. 65\nTexas Southern 66\nAppalachian St. 67\n"
  buf = io.StringIO(team_str)
  id_dict = {}
  for i in range(68):
    line = buf.readline().rstrip()
    name, id = line.rsplit(' ', 1)
    id_dict[int(id)] = name
  return id_dict

id_dict = gen_map()


# To prevent from using a blueprint, we use a cyclic import
# This also means that we need to place this import here
# pylint: disable=cyclic-import, wrong-import-position
from app import routes