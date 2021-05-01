import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
#from flaskr import create_app
from flask import request, abort
from models import setup_db, Actors, Movies

class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('saadshamim', 'hello', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        db.create_all()

        self.new_actor = {
        'name': 'Saad Shamim',
        'age': '23',
        'gender': 'Male'
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

    def test_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

#    def test_create_actors(self):
#        res = self.client().post('/actors', json=self.new_actor)
#        data = json.loads(res.data)
#
#        self.assertEqual(res.status_code, )


