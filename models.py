from flask_sqlalchemy import SQLAlchemy
import dateutil.parser

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
    db.create_all()
    # db_drop_and_create_all()


'''
Person
Have title and release year
'''

cast = db.Table(
    'cast',
    db.Column('actor_id', db.Integer, db.ForeignKey('actors.id')),
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'))
)


class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(1))  # 🚧 create ENUM

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

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def update():
        db.session.commit()


def __repr__(self):
    return f'<Movie id: "{self.id}", name: "{self.name}"'


class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    actors = db.relationship(
        'Actor',
        secondary=cast,
        backref=db.backref('movies')
    )

    def __init__(self, name, release_date):
        self.title = title
        self.release_date = release_date

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date}

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def update():
        db.session.commit()

    def __repr__(self):
        return f'<Movie id: "{self.id}", title: "{self.title}"'
