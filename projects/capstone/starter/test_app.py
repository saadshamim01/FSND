import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from app import create_app
from flask import request, abort
from models import setup_db, Actor, Movie

NONE = 'No_permission'
BASIC = os.environ["CASTING_ASSISTANT"]
INTERMEDIATE = os.environ["CASTING_DIRECTOR"]
ADVANCE = os.environ["EXECUTIVE_PRODUCER"]


class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('saadshamim', 'hello', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        #db.create_all()

        self.new_actor = {
        'name': 'Saad Shamim',
        'age': '23',
        'gender': 'Male'
        }
        self.new_movie = {
        "title": "Hercules",
        "release_date": "2022-12-12 23:23:23"
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            #create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_for_home(self):
        res = self.client().get('/')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


###################################################################
###GET TEST FOR ACTOR & MOVIE
###################################################################


    def test_get_actors(self):
        #res = self.client().get('/actors')
        res = self.client().get('/actors',
                                headers={'Authorization': f'Bearer {BASIC}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_movies(self):
        res = self.client().get('/movies',
                                headers={'Authorization': f'Bearer {BASIC}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

###TEST FOR 401 FAILED GET ACTOR & MOVIE

    def test_401_get_actor_permission_not_found(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'JWT not found')

    def test_401_get_movie_permission_not_found(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'JWT not found')

###TEST FOR 403 FAILED GET ACTOR & MOVIE


###################################################################
###POST TEST FOR ACTOR & MOVIE
###################################################################


    def test_create_actors(self):
        res = self.client().post('/actors',
                                 headers={'Authorization': f'Bearer {INTERMEDIATE}'},
                                 json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['create'])

    def test_create_movie(self):
        res = self.client().post('/movies',
                                 headers={'Authorization': f'Bearer {INTERMEDIATE}'},
                                 json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['create'])

###TEST FOR 405 FAILED POST ACTOR & MOVIE

    def test_405_if_actor_creation_not_allowed(self):
        res = self.client().post('actors/2',
                                 headers={'Authorization': f'Bearer {INTERMEDIATE}'},
                                 json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_405_if_movie_creation_not_allowed(self):
        res = self.client().post('movies/2',
                                 headers={'Authorization': f'Bearer {INTERMEDIATE}'},
                                 json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

###TEST FOR 401 FAILED POST ACTOR & MOVIE

    def test_401_post_actor_permission_not_found(self):
        res = self.client().post('/actors',json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'JWT not found')

    def test_401_post_movie_permission_not_found(self):
        res = self.client().post('/actors',json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'JWT not found')

###TEST FOR 403 FAILED POST ACTOR & MOVIE

    def test_403_post_actor_authorization_permission_not_found(self):
        res = self.client().post('/actors', headers={'Authorization': f'Bearer {BASIC}'}, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_403_post_movie_authorization_permission_not_found(self):
        res = self.client().post('/movies', headers={'Authorization': f'Bearer {BASIC}'}, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

###################################################################
###PATCH TEST FOR ACTOR & MOVIE
###################################################################


    def test_update_actor(self):
        res = self.client().patch('/actors/3',
                                  headers={'Authorization': f'Bearer {INTERMEDIATE}'},
                                  json={'name':'Rober Downney Jr.'})
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == 3).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['edit'])

    def test_update_movie(self):
        res = self.client().patch('/movies/2',
                                  headers={'Authorization': f'Bearer {INTERMEDIATE}'},
                                  json={'title':'Age of Ultron'})
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['edit'])

###TEST FOR FAILED PATCH ACTOR & MOVIE

    def test_400_for_failed_actor_update(self):
        res = self.client().patch('/actors/2',
                                  headers={'Authorization': f'Bearer {INTERMEDIATE}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')


    def test_400_for_failed_movie_update(self):
        res = self.client().patch('/movies/2',
                                  headers={'Authorization': f'Bearer {INTERMEDIATE}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

###TEST FOR 401 FAILED PATCH ACTOR & MOVIE

    def test_401_patch_actor_permission_not_found(self):
        res = self.client().patch('/actors/3', json={'name':'Rober Downney Jr.'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'JWT not found')

    def test_401_patch_movie_permission_not_found(self):
        res = self.client().patch('/movies/4', json={'title':'Age of Ultron'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'JWT not found')

###TEST FOR 403 FAILED PATCH ACTOR & MOVIE

    def test_403_patch_actor_authorization_permission_not_found(self):
        res = self.client().patch('/actors/3', headers={'Authorization': f'Bearer {BASIC}'}, json={'name':'Rober Downney Jr.'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_403_post_movie_authorization_permission_not_found(self):
        res = self.client().patch('/movies/2', headers={'Authorization': f'Bearer {BASIC}'}, json={'title':'Age of Ultron'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')


###################################################################
###DELETE TEST FOR ACTOR & MOVIE
###################################################################


#    def test_delete_actor(self):
#        res = self.client().delete('/actors/9',
#                                   headers={'Authorization': f'Bearer {ADVANCE}'})
#        data = json.loads(res.data)
#
#        actor = Actor.query.filter(Actor.id == 9).one_or_none()
#
#        self.assertEqual(res.status_code, 200)
#        self.assertEqual(data['success'], True)
#        self.assertTrue(data['delete'])
#
#    def test_delete_movie(self):
#        res = self.client().delete('/movies/9',
#                                   headers={'Authorization': f'Bearer {ADVANCE}'})
#        data = json.loads(res.data)
#
#        movie = Movie.query.filter(Movie.id == 9).one_or_none()
#        self.assertEqual(res.status_code, 200)
#        self.assertEqual(data['success'], True)
#        self.assertTrue(data['delete'])

###FAILED DELETE TEST FOR ACTOR & MOVIE

    def test_422_if_actor_does_not_exist(self):
        res = self.client().delete('/actors/1000',
                                   headers={'Authorization': f'Bearer {ADVANCE}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'unprocessable' )

    def test_422_if_movie_does_not_exit(self):
        res = self.client().delete('/movies/1000',
                                   headers={'Authorization': f'Bearer {ADVANCE}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

###FAILED 401 DELETE TEST FOR ACTOR & MOVIE

    def test_401_delete_actor_permission_not_found(self):
        res = self.client().delete('actors/9')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'JWT not found')

    def test_401_delete_movie_permission_not_found(self):
        res = self.client().delete('movies/9')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'JWT not found')

###FAILED 403 DELETE TEST FOR ACTOR & MOVIE

    def test_403_delete_actor_authorization_permission_not_found(self):
        res = self.client().delete('/actors/21', headers={'Authorization': f'Bearer {INTERMEDIATE}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_403_delete_movie_authorization_permission_not_found(self):
        res = self.client().delete('/movies/9', headers={'Authorization': f'Bearer {INTERMEDIATE}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')


if __name__ == "__main__":
    unittest.main()


