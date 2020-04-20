import os
import unittest
import json
import sys
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from config import TestDBConfig
# remove db and dbdropandcreate
from models import db, db_drop_and_create_all, setup_db, Actor, Movie


class ApiTestCase(unittest.TestCase):
    """ Represents the api test case """

    def insert_data(self):
        """Seed test database with initial data"""
        actor1 = Actor(name="Sam Jones", age=25, gender='m')
        actor2 = Actor(name="Cynthia Jones", age=22, gender='f')
        actor3 = Actor(name="Vanna White", age=32, gender='f')

        movie1 = Movie(title="The Movie", year=2015)
        movie2 = Movie(title="The Movie 2", year=2016)
        movie3 = Movie(title="The Movie 3", year=2017)

        actor1.insert()
        actor2.insert()
        actor3.insert()
        movie1.insert()
        movie2.insert()
        movie3.insert()

        self.db.session.commit()
        self.db.session.close()

    def setup(self):
        """ Configure test client with app & db """
        self.app = create_app()
        self.client = self.app.test_client
        # self.database_path = os.getenv('TEST_DATABASE_URL')
        self.database_path = 'postgres://bunty@localhost:5432/casting_test'
        self.headers = {
            'Authorization': f'Bearer {os.getenv("EXEC_PROD_TOKEN")}'
        }
        setup_db(self.app, None, database_path=self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            # self.app.config["TESTING"] = True
            # self.app.config["SQLALCHEMY_DATABASE_URI"] = self.database_path
            # self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
            # sys.stdout = sys.__stdout__
            # print('from unittest')
            self.db.app = self.app
            self.db.init_app(self.app)
            self.db.create_all()

        # self.insert_data()

    # def setup(self):
    #     self.app = create_app()  # 'config.TestDBConfig'
    #     self.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://bunty@localhost:5432/casting_test'
    #     self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #     self.api.app_context().push()
    #     self.client = self.app.test_client
    #     self.headers = {
    #         'Authorization': f'Bearer {os.getenv("EXEC_PROD_TOKEN")}'
    #     }

    #     self.db = SQLAlchemy()
    #     self.db.init_app(self.app)

    #     self.db.session.commit()
    #     self.db.drop_all()
    #     self.db.create_all()

    #     self.insert_data()

    def tearDown(self):
        """Runs cleanup after each test"""
        # self.db.session.rollback()
        # self.db.drop_all()
        # self.db.session.close()
        pass

    def test_test(self):
        self.assertEqual(True, True)

    # def test_db(self):
    #     """Test if the db gets populated correctly"""
    #     actors = Actor.query.all()  # get all actors
    #     # test if actors is a list
    #     self.assertEqual(isinstance(actors, list), True)
    #     # test if the first item is an Actor
    #     self.assertEqual(isinstance(actors[0], Actor), True)
    #     movies = Movie.query.all()  # get all movies
    #     # test if movies is a list
    #     self.assertEqual(isinstance(movies, list), True)
    #     # test if the first item is an Actor
    #     self.assertEqual(isinstance(movies[0], Movie), True)


if __name__ == '__main__':
    unittest.main()
