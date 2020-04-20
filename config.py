# import os
# basedir = os.path.abspath(os.path.dirname(__file__))

# database_name = "casting"

# '''
# local_db = 'postgres://bunty@localhost:5432/casting'
# heroku_db = 'postgres://domxhljotpyuck:046e562a3389dd0888da6cc19cc4efcc20640f94f566aa0c8b262f0296b22008@ec2-34-200-116-132.compute-1.amazonaws.com:5432/d4ik1oq9u89jsb'
# '''


# class DBConfig:
#     DEBUG = True
#     SECRET_KEY = os.urandom(32)
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

#     def __repr__(self):
#         return f'<DBonfig DEBUG: "{self.DEBUG}", SECRET_KEY: "{self.SECRET_KEY}", SQLALCHEMY_TRACK_MODIFICATIONS: "{self.SQLALCHEMY_TRACK_MODIFICATIONS}", SQLALCHEMY_DATABASE_URI: "{self.SQLALCHEMY_DATABASE_URI}">'


# class TestDBConfig:
#     DEBUG = True
#     SECRET_KEY = os.urandom(32)
#     TESTING = True
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL')

#     def __repr__(self):
#         return f'<DBonfig DEBUG: "{self.DEBUG}", SECRET_KEY: "{self.SECRET_KEY}", SQLALCHEMY_TRACK_MODIFICATIONS: "{self.SQLALCHEMY_TRACK_MODIFICATIONS}", SQLALCHEMY_DATABASE_URI: "{self.SQLALCHEMY_DATABASE_URI}">'


# class Auth0Config:
#     domain = os.getenv('AUTH0_DOMAIN')
#     algorithms = os.getenv('AUTH0_ALGORITHMS')
#     audience = os.getenv('AUTH0_AUDIENCE')

#     def __repr__(self):
#         return f'<Auth0Config domain: "{domain}", algorithms: "{algorithms}", doman: "{audience}">'
