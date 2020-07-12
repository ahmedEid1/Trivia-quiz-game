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
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

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

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertGreater(len(data['categories']), 0)

    def test_wrong_method(self):
        res = self.client().post('/categories')
        self.assertEqual(res.status_code, 405)

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertGreater(len(data['questions']), 0)

    def test_zero_questions(self):
        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

    def test_question_delete(self):
        res = self.client().delete('/questions/5')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['id'], 5)

    def test_400_bad_delete(self):
        res = self.client().delete('/questions/1000')
        self.assertEqual(res.status_code, 400)

    def test_question_insert(self):
        info = {
            'question': "how are you",
            'answer': "fine",
            'category': 4,
            'difficulty': 1
        }
        res = self.client().post('/questions/add', data=json.dumps(info), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['question']), 5)

    def test_not_complete_question_insert(self):
        info = {
            'answer': "fine",
            'category': 4,
            'difficulty': 1
        }
        res = self.client().post('/questions/add', data=json.dumps(info), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['message'], "Bad Request")

    def test_search_word(self):
        info = {
            'searchTerm': "1"
        }
        res = self.client().post('/questions', data=json.dumps(info), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertGreater(len(data['questions']), 0)

    def test_searchTerm_not_str(self):
        info = {
            'searchTerm': 1
        }
        res = self.client().post('/questions', data=json.dumps(info), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 500)

    def test_get_questions_by_category(self):
        res = self.client().get("categories/5/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertGreater(len(data['questions']), 0)

    def test_404_category_not_found(self):
        res = self.client().get("categories/100/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], "Not Found")

    def test_get_quiz_question(self):
        info = {
            "quiz_category": {
                "id": 2,
            },
            "previous_questions": [1, 2, 3]
        }
        res = self.client().post("/quizzes", data=json.dumps(info), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['question']), 5)

    def test_wrong_category_id(self):
        info = {
            "quiz_category": {
            },
            "previous_questions": [1, 2, 3]
        }
        res = self.client().post("/quizzes", data=json.dumps(info), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['message'], "Bad Request")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
