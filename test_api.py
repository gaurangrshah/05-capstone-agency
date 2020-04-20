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

print(EXEC_PROD_TOKEN)


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

        self.db.session.add(actor1)
        self.db.session.add(actor2)
        self.db.session.add(actor3)

        self.db.session.add(movie1)
        self.db.session.add(movie2)
        self.db.session.add(movie3)
        self.db.session.commit()
        self.db.session.close()

    def setUp(self):
        """ Configure test client with app & db """
        self.app = create_app()

        self.client = self.app.test_client
        self.token = f"Bearer {EXEC_PROD_TOKEN}"
        self.headers = {
            'Authorization': f'Bearer {EXEC_PROD_TOKEN}'}

        setup_db(self.app, database_path=database_path)

        with self.app.app_context():
            self.db = db

            self.db.drop_all()
            self.db.create_all()

            self.insert_data()

    def tearDown(self):
        """Runs cleanup after each test"""
        self.db.session.rollback()
        self.db.drop_all()
        self.db.session.close()
        pass

    def test_test(self):
        """Test if tests are setup"""
        self.assertEqual(True, True)

    def test_seed_testdb(self):
        """Test Seed Data in Db"""
        actors = Actor.query.all()  # check of actors is a list of Actors
        self.assertEqual(isinstance(actors, list), True)
        self.assertEqual(isinstance(actors[0], Actor), True)
        movies = Movie.query.all()  # check of movies is a list of Movies
        self.assertEqual(isinstance(movies, list), True)
        self.assertEqual(isinstance(movies[0], Movie), True)

    def test_get_actors_with_NO_HEADERS(self):
        res = self.client().get('/api/actors')
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['error'], 'Authorization header is expected.')

    def test_post_actors_with_NO_HEADERS(self):
        res = self.client().post('/api/actors', json={
            'name': 'Tom Smith',
            'age': 34,
            'gender': 'm'
        })
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['error'], 'Authorization header is expected.')

    def test_patch_actors_with_NO_HEADERS(self):
        res = self.client().patch('/api/actors/4', json={
            'name': 'Jane Smith',
            'age': 24,
            'gender': 'f'
        })
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['error'], 'Authorization header is expected.')

    def test_get_actors_with_NO_HEADERS(self):
        res = self.client().get('/api/actors/4')
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['error'], 'Authorization header is expected.')

    def test_delete_actors_with_NO_HEADERS(self):
        res = self.client().delete('/api/actors/4')
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['error'], 'Authorization header is expected.')

    # def test_get_actors(self):
    #     self.client().get('/api/actors',  headers={
    #         "Authorization": 'bearer '+EXEC_PROD_TOKEN})
    #     # body = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
        # self.assertEqual(body['error'], 'Authorization header is expected.')

    # def test_post_actors(self):
    #     res = self.client().post('/api/actors', headers=self.headers, json={
    #         'name': 'Tom Smith',
    #         'age': 34,
    #         'gender': 'm'
    #     })
    #     body = json.loads(res.data)
    #     self.assertEqual(res.status_code, 401)
    #     self.assertEqual(body['error'], 'Authorization header is expected.')

    # def test_patch_actors(self):
    #     res = self.client().patch('/api/actors/4', headers=self.headers, json={
    #         'name': 'Jane Smith',
    #         'age': 24,
    #         'gender': 'f'
    #     })
    #     body = json.loads(res.data)
    #     self.assertEqual(res.status_code, 401)
    #     self.assertEqual(body['error'], 'Authorization header is expected.')

    # def test_get_actors(self):
    #     res = self.client().get('/api/actors/4', headers=self.headers)
    #     body = json.loads(res.data)
    #     self.assertEqual(res.status_code, 401)
    #     self.assertEqual(body['error'], 'Authorization header is expected.')

    # def test_delete_actors(self):
    #     res = self.client().delete('/api/actors/4', headers=self.headers)
    #     body = json.loads(res.data)
    #     self.assertEqual(res.status_code, 401)
    #     self.assertEqual(body['error'], 'Authorization header is expected.')

# ---------------------------------------------------------------------------------
# ---------------------------------- MOVIES ---------------------------------------
# ---------------------------------------------------------------------------------

    def test_get_movies_with_NO_HEADERS(self):
        res = self.client().get('/api/movies')
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['error'], 'Authorization header is expected.')

    def test_post_movies_with_NO_HEADERS(self):
        res = self.client().post('/api/movies', json={
            'title': 'The Movie 4',
            'year': 2017
        })
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['error'], 'Authorization header is expected.')

    def test_patch_movies_with_NO_HEADERS(self):
        res = self.client().patch('/api/movies/4', json={
            'title': 'The Movie 4',
            'year': 2018
        })
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['error'], 'Authorization header is expected.')

    def test_get_movies_with_NO_HEADERS(self):
        res = self.client().get('/api/movies/4')
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['error'], 'Authorization header is expected.')

    def test_delete_movies_with_NO_HEADERS(self):
        res = self.client().delete('/api/movies/4')
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(body['error'], 'Authorization header is expected.')


if __name__ == '__main__':
    unittest.main()
