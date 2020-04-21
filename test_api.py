import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import db, setup_db, Actor, Movie
from dotenv import load_dotenv
# https://www.nylas.com/blog/making-use-of-environment-variables-in-python/
load_dotenv()

EXEC_PROD_TOKEN = os.environ['EXEC_PROD_TOKEN']
CAST_DIR_TOKEN = os.environ['CAST_DIR_TOKEN']
CAST_ASST_TOKEN = os.environ['CAST_ASST_TOKEN']

prod_database_path = os.environ['PROD_DATABASE_URL']
database_path = os.environ['TEST_DATABASE_URL']


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

# ---------------------------------------------------------------------------------
# ------------------------------ SETUP TESTS --------------------------------------
# ---------------------------------------------------------------------------------

    def setUp(self):
        """ Configure test client with app & db """
        self.app = create_app()

        self.client = self.app.test_client
        self.prod_headers = {"Authorization": "Bearer {}".format(EXEC_PROD_TOKEN)}
        self.dir_headers = {"Authorization": "Bearer {}".format(CAST_DIR_TOKEN)}
        self.asst_headers = {"Authorization": "Bearer {}".format(CAST_ASST_TOKEN)}


        setup_db(self.app, database_path=prod_database_path)

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

# ---------------------------------------------------------------------------------
# --------------------------------- TEST DB ---------------------------------------
# ---------------------------------------------------------------------------------

    def test_seed_testdb(self):
        """Test Seed Data in Db"""
        actors = Actor.query.all()  # check of actors is a list of Actors
        self.assertEqual(isinstance(actors, list), True)
        self.assertEqual(isinstance(actors[0], Actor), True)
        movies = Movie.query.all()  # check of movies is a list of Movies
        self.assertEqual(isinstance(movies, list), True)
        self.assertEqual(isinstance(movies[0], Movie), True)

# ---------------------------------------------------------------------------------
# ------------------------ UNAUTHENTICATED ACTORS ---------------------------------
# ---------------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------------
# ------------------------------- PRODUCER ACTORS ---------------------------------
# ---------------------------------------------------------------------------------

    def test_get_actors(self):
        res = self.client().get(
            '/api/actors', headers=self.prod_headers)

        body = json.loads(res.data)
        actors = body['actors']
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(isinstance(actors, list), True)

    def test_post_actors(self):
        res = self.client().post('/api/actors', headers=self.prod_headers, json={
            'name': 'Tom Smith',
            'age': 34,
            'gender': 'm'
        })
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    def test_patch_actors(self):
        res = self.client().patch('/api/actors/2', headers=self.prod_headers, json={
            'name': 'Jane Smith',
            'age': 24,
            'gender': 'f'
        })
        body = json.loads(res.data)
        actors = body['actors']
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(isinstance(actors, list), True)

    def test_get_actors(self):
        res = self.client().get('/api/actors/2', headers=self.prod_headers)
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    def test_delete_actors(self):
        res = self.client().delete('/api/actors/2', headers=self.prod_headers)
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

# ---------------------------------------------------------------------------------
# ------------------------------- DIRECTOR ACTORS ---------------------------------
# ---------------------------------------------------------------------------------

    def test_get_actors(self):
        res = self.client().get(
            '/api/actors', headers=self.dir_headers)

        body = json.loads(res.data)
        actors = body['actors']
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(isinstance(actors, list), True)

    def test_post_actors(self):
        res = self.client().post('/api/actors', headers=self.dir_headers, json={
            'name': 'Tom Smith',
            'age': 34,
            'gender': 'm'
        })
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    def test_patch_actors(self):
        res = self.client().patch('/api/actors/2', headers=self.dir_headers, json={
            'name': 'Jane Smith',
            'age': 24,
            'gender': 'f'
        })
        body = json.loads(res.data)
        actors = body['actors']
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(isinstance(actors, list), True)

    def test_get_actors(self):
        res = self.client().get('/api/actors/2', headers=self.dir_headers)
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    def test_delete_actors(self):
        res = self.client().delete('/api/actors/2', headers=self.dir_headers)
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)



# ---------------------------------------------------------------------------------
# ------------------------------ ASSISTANT ACTORS ---------------------------------
# ---------------------------------------------------------------------------------

    def test_get_actors(self):
        res = self.client().get(
            '/api/actors', headers=self.asst_headers)

        body = json.loads(res.data)
        actors = body['actors']
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(isinstance(actors, list), True)

    def test_post_actors(self):
        """ FAILS: 401 - UNAUTHORIZED """
        res = self.client().post('/api/actors', headers=self.asst_headers, json={
            'name': 'Tom Smith',
            'age': 34,
            'gender': 'm'
        })

        self.assertEqual(res.status_code, 401)

    def test_patch_actors(self):
        """ FAILS: 401 - UNAUTHORIZED """
        res = self.client().patch('/api/actors/2', headers=self.asst_headers, json={
            'name': 'Jane Smith',
            'age': 24,
            'gender': 'f'
        })

        self.assertEqual(res.status_code, 401)

    def test_get_actors(self):
        res = self.client().get('/api/actors/2', headers=self.asst_headers)
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    def test_delete_actors(self):
        """ FAILS: 401 - UNAUTHORIZED """
        res = self.client().delete('/api/actors/2', headers=self.asst_headers)

        self.assertEqual(res.status_code, 401)


# ---------------------------------------------------------------------------------
# --------------------------- UNAUTHENTICATED MOVIES ------------------------------
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

# ---------------------------------------------------------------------------------
# ------------------------------- PRODUCER MOVIES ---------------------------------
# ---------------------------------------------------------------------------------

    def test_get_movies(self):
        res = self.client().get(
            '/api/movies', headers=self.prod_headers)

        body = json.loads(res.data)
        movies = body['movies']
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(isinstance(movies, list), True)

    def test_post_movies(self):
        res = self.client().post('/api/movies', headers=self.prod_headers, json={
            'title': 'The Movie 4',
            'year': 2017
        })
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    def test_patch_movies(self):
        res = self.client().patch('/api/movies/2', headers=self.prod_headers, json={
            'title': 'The Movie 4',
            'year': 2018
        })
        body = json.loads(res.data)
        movies = body['movies']
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(isinstance(movies, list), True)

    def test_get_movies(self):
        res = self.client().get('/api/movies/2', headers=self.prod_headers)
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    def test_delete_movies(self):
        res = self.client().delete('/api/movies/2', headers=self.prod_headers)
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

# ---------------------------------------------------------------------------------
# ------------------------------- DIRECTOR MOVIES ---------------------------------
# ---------------------------------------------------------------------------------

    def test_get_movies(self):
        res = self.client().get(
            '/api/movies', headers=self.dir_headers)

        body = json.loads(res.data)
        movies = body['movies']
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(isinstance(movies, list), True)

    def test_post_movies(self):
        """ FAILS: 401 - UNAUTHORIZED """
        res = self.client().post('/api/movies', headers=self.dir_headers, json={
            'title': 'The Movie 4',
            'year': 2017
        })
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_patch_movies(self):
        res = self.client().patch('/api/movies/2', headers=self.dir_headers, json={
            'title': 'The Movie 4',
            'year': 2018
        })
        body = json.loads(res.data)
        movies = body['movies']
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(isinstance(movies, list), True)

    def test_get_movies(self):
        res = self.client().get('/api/movies/2', headers=self.dir_headers)
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    def test_delete_movies(self):
        """ FAILS: 401 - UNAUTHORIZED """
        res = self.client().delete('/api/movies/2', headers=self.dir_headers)
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

# ---------------------------------------------------------------------------------
# ------------------------------ ASSISTANT MOVIES ---------------------------------
# ---------------------------------------------------------------------------------

    def test_get_movies(self):
        res = self.client().get(
            '/api/movies', headers=self.asst_headers)

        body = json.loads(res.data)
        movies = body['movies']

        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(isinstance(movies, list), True)

    def test_post_movies(self):
        """ FAILS: 401 - UNAUTHORIZED """
        res = self.client().post('/api/movies', headers=self.asst_headers, json={
            'title': 'The Movie 4',
            'year': 2017
        })

        self.assertEqual(res.status_code, 401)

    def test_patch_movies(self):
        """ FAILS: 401 - UNAUTHORIZED """
        res = self.client().patch('/api/movies/2', headers=self.asst_headers, json={
            'title': 'The Movie 4',
            'year': 2018
        })

        self.assertEqual(res.status_code, 401)

    def test_get_movies(self):
        res = self.client().get('/api/movies/2', headers=self.asst_headers)
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    def test_delete_movies(self):
        """ FAILS: 401 - UNAUTHORIZED """
        res = self.client().delete('/api/movies/2', headers=self.asst_headers)
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

if __name__ == '__main__':
    unittest.main()
