import os
from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json


database_name = "casting"

heroku_db = "postgres://domxhljotpyuck:046e562a3389dd0888da6cc19cc4efcc20640f94f566aa0c8b262f0296b22008@ec2-34-200-116-132.compute-1.amazonaws.com:5432/d4ik1oq9u89jsb"
# database_path = database_url

local_db = "postgres://{}:{}@{}/{}".format(
    'postgres', 'bunty', 'localhost:5432', database_name)

# if os.environ['DATABASE_URL']:
#     db_from_vars = os.environ['DATABASE_URL']

database_path = local_db


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


class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String)
    age = Column(db.Integer)
    gender = Column(db.String)  # 🚧 create ENUM

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender}


class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(db.Integer, primary_key=True)
    title = Column(db.String)
    release_date = Column(db.String)

    def __init__(self, name, release_date):
        self.title = title
        self.release_date = release_date

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date}
