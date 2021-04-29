import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('saadshamim', 'hello', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
                          'question': 'Number of planets in the universe',
                          'answer': '8',
                          'category': '1',
                          'difficulty': '5'
                          }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_paginated_questions(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_sent_request_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000', json={'difficulty': 4})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_question(self):
        res = self.client().delete('/questions/17')
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == 17).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 17)
        self.assertTrue(data['total_questions'])
        self.assertEqual(question, None)

    def test_404_if_question_does_not_exist(self):
        res = self.client().delete('questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_create_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['questions']))

    def test_405_if_question_creation_not_allowed(self):
        res = self.client().post('/questions/45', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

#    def test_get_question_search_with_results(self):
#        res = self.client().post('/search', json={'search': 'organ'})
#        data = json.loads(res.data)
#
#        self.assertEqual(res.status_code, 200)
#        self.assertEqual(data['success'], True)
#        self.assertTrue(data['total_questions'])
#        self.assertEqual(len(data['questions']), 1)
#
#    def test_get_question_search_without_results(self):
#        res = self.client().post('/search', json={'search': 'lol'})
#        data = json.loads(res.data)
#
#        self.assertEqual(res.status_code, 200)
#        self.assertEqual(data['success'], True)
#        self.assertEqual(data['total_questions'], 0)
#        self.assertEqual(len(data['total_questions']), 0)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()