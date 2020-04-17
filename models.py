import os
from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json


database_name = "cap-agency"
# database_path = "postgres://{}:{}@{}/{}".format(
#     'postgres', 'bunty', 'localhost:5432', database_name)

database_url = "postgres://domxhljotpyuck:046e562a3389dd0888da6cc19cc4efcc20640f94f566aa0c8b262f0296b22008@ec2-34-200-116-132.compute-1.amazonaws.com:5432/d4ik1oq9u89jsb"

# database_path = os.environ['DATABASE_URL']
database_path = database_url

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


'''
Person
Have title and release year
'''


class Person(db.Model):
    __tablename__ = 'People'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String)
    catchphrase = Column(db.String)

    def __init__(self, name, catchphrase=""):
        self.name = name
        self.catchphrase = catchphrase

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'catchphrase': self.catchphrase}
