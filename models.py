from flask_sqlalchemy import SQLAlchemy
import dateutil.parser
from flask_migrate import Migrate

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


def setup_db(app):
    db.app = app
    db.init_app(app)
    # db.create_all()
    # db_drop_and_create_all()


'''
Person
Have title and release year
'''

cast = db.Table(
    'cast',
    db.Column('movie_id', db.Integer,
              db.ForeignKey('actors.id'), primary_key=True),
    db.Column('actor_id', db.Integer,
              db.ForeignKey('movies.id'), primary_key=True),
)


class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(1))  # 🚧 create ENUM
    cast = db.relationship('Movie', secondary=cast,
                           backref=db.backref('movies', lazy=True))

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender}

    def __repr__(self):
        return f'<Actor id: "{self.id}", name: "{self.name}">'


class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String)
    # release_date = db.Column(db.DateTime)
    cast = db.relationship('Actor', secondary=cast,
                           backref=db.backref('actors', lazy=True))

    def __init__(self, title):  # add arg: release_date
        self.title = title
        # self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            # 'release_date': self.release_date.strftime('%c')
        }

    def __repr__(self):
        return f'<Movie id: "{self.id}", title: "{self.title}, "cast": "{self.cast}">'
