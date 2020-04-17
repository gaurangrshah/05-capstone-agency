import os

basedir = os.path.abspath(os.path.dirname(__file__))

database_name = "casting"

heroku_db = 'postgres://domxhljotpyuck:046e562a3389dd0888da6cc19cc4efcc20640f94f566aa0c8b262f0296b22008@ec2-34-200-116-132.compute-1.amazonaws.com:5432/d4ik1oq9u89jsb'

formatted_local_db = 'postgres://{}:{}@{}/{}'.format(
    'postgres', 'bunty', 'localhost:5432', database_name)

local_db = 'postgres://postgres:bunty@localhost:5432/casting'

# database_path = os.getenv('DATABASE_URL')


class db_config:
    DEBUG = True
    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

    print('debug:', DEBUG, 'SECRET_KEY:', SECRET_KEY, 'SQLALCHEMY_TRACK_MODIFICATIONS:',
          SQLALCHEMY_TRACK_MODIFICATIONS, 'SQLALCHEMY_DATABASE_URI:', SQLALCHEMY_DATABASE_URI)

    # class auth0_config:
    #     domain = os.environ['AUTH0_DOMAIN']
    #     algorithms = os.environ['AUTH0_ALGORITHMS']
    #     audience = os.environ['AUTH0_AUDIENCE']
