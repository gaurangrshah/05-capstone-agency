import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import db, setup_db, Actor, Movie
from dotenv import load_dotenv

# basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv()

TESTING = True
EXEC_PROD_TOKEN = os.environ.get('EXEC_PROD_TOKEN')
database_path = os.environ.get('TEST_DATABASE_URL')

# print("EXEC_PROD_TOKEN", EXEC_PROD_TOKEN)


class ApiTestCase(unittest.TestCase):
    """ Represents the api test case """

    # def inserts(self):
    #     """Seed test database with initial data"""
    #     actor1 = Actor(name="Sam Jones", age=25, gender='m')
    #     actor2 = Actor(name="Cynthia Jones", age=22, gender='f')
    #     actor3 = Actor(name="Vanna White", age=32, gender='f')

    #     movie1 = Movie(title="The Movie", year=2015)
    #     movie2 = Movie(title="The Movie 2", year=2016)
    #     movie3 = Movie(title="The Movie 3", year=2017)

    #     # actor1.insert()
    #     # actor2.insert()
    #     # actor3.insert()
    #     # movie1.insert()
    #     # movie2.insert()
    #     # movie3.insert()

    #     self.db.session.add(actor1)
    #     self.db.session.add(actor2)
    #     self.db.session.add(actor3)

    #     self.db.session.add(movie1)
    #     self.db.session.add(movie2)
    #     self.db.session.add(movie3)
    #     self.db.session.close()

    def setUp(self):
        """ Configure test client with app & db """
        self.app = create_app()
        self.client = self.app.test_client
        self.headers = {
            'Authorization': f'Bearer {EXEC_PROD_TOKEN}'
        }
        setup_db(self.app, database_path=database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            # self.app.config["TESTING"] = TESTING
            self.db.init_app(self.app)
            # self.db.drop_all()
            self.db.create_all()

            # self.inserts()

    def tearDown(self):
        """Runs cleanup after each test"""
        # self.db.session.rollback()
        # self.db.drop_all()
        # self.db.session.close()
        pass

    def test_test(self):
        """Test if tests are setup"""
        self.assertEqual(True, True)

    def test_get_actors(self):
        """Test get actors"""
        r = self.client().get('/api/actors', headers=self.headers)
        self.assertEqual(r.status_code, 200)


if __name__ == '__main__':
    unittest.main()
