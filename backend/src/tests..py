import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from .auth.auth import AuthError, requires_auth
from .lib import *


class ShopeTestCase(unittest.TestCase):
    """This class represents the coffee shop test cases"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        database_filename = "test_database.db"
        project_dir = os.path.dirname(os.path.abspath(__file__))
        default_database_path = "sqlite:///database.db".format(os.path.join(project_dir, database_filename))

        setup_db(self.app, self.default_database_path)

        # # Category related variables
        # self.search_category = 'new_category'
        #
        # self.new_category = {
        #     'type': 'new_category'
        #     }
        #
        # # Question related variables
        # self.search_question = 'a'
        self.delete_drink = 'Delete me!'
        #
        self.new_drink = {
            'title': 'brand new drink',
            'recipe':
                [{'color': 'blue', 'name':'blue', 'parts':1},
                 {'color': 'red', 'name':'red', 'parts':3},
                ]
            }

        self.new_drink_for_update = {
            'title': 'update drink',
            'recipe':
                [{'color': 'blue', 'name':'blue', 'parts':1},
                 {'color': 'white', 'name':'red', 'parts':3},
                ]
            }

        self.updated_drink = {
            'title': 'update drink',
            'recipe':
                [{'color': 'blue', 'name':'blue', 'parts':1},
                 {'color': 'white', 'name':'red', 'parts':3},
                ]
            }

        # self.new_question_for_search = {
        #     'question': 'Will I be deleted?',
        #     'answer': 'Unanswerable',
        #     'category': 2,
        #     'difficulty': 1
        #     }

        self.new_question_for_delete = {
            'title': self.delete_drink,
            'recipe':
                [{'color': 'blue', 'name':'blue', 'parts':1},
                 {'color': 'white', 'name':'red', 'parts':3},
                ]
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

    """ Begin Test Suit """

    #------------------------------------------------------------------------------------#
    # Get: Short version of drinks
    #------------------------------------------------------------------------------------#
    def test_get_drinks(self):
        """Test Get Drinks """
        # print('...Get categories...')
        res = self.client().get('/drinks')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total'])
        self.assertTrue(data['drinks'])

    #------------------------------------------------------------------------------------#
    # Get: Long version of drinks
    #------------------------------------------------------------------------------------#
    def test_get_drinks_detailed(self):
        """Test Get Detailed drinks"""
        # print('...Get questions...')
        res = self.client().get('/drinks-detail')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    # #------------------------------------------------------------------------------------#
    # # Add: Success
    # #------------------------------------------------------------------------------------#
    def test_add_drink(self):
        """Test Add Drink """
        # print('...Add question...')
        res = self.client().post('/drinks', json=self.new_drink, follow_redirects=True)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['drinks'], True)

    # #------------------------------------------------------------------------------------#
    # # Update: Success
    # #------------------------------------------------------------------------------------#
    def test_update_drink(self):
        """Test Update Drink """
        # print('...Add question...')
        res = self.client().post('/drinks', json=self.new_drink_for_update)
        item = json.loads(res.data).get('id', None)
        res = self.clinet().patch('/drinks/' + items, json=self.updated_drink)


    # #------------------------------------------------------------------------------------#
    # # Delete: Success
    # #------------------------------------------------------------------------------------#
    def test_del_drink(self):
        """Test Delete Question """
        # print('...Delete question...')
        res = self.client().post('/drinks', json=self.new_question_for_delete)
        res = self.client().post('/drinks/search', json={'searchTerm': self.delete_drink})
        item = json.loads(res.data).get('drinks', None)
        res = self.client().delete('/drinks/' + str(item[0]['id']))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # #------------------------------------------------------------------------------------#
    # # Delete: Failure
    # #------------------------------------------------------------------------------------#
    def test_del_question_404(self):
        """Test Delete Question """
        res = self.client().delete('/drinks/' + str(-1))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

#     # #------------------------------------------------------------------------------------#
#     # # Quizzes: Success
#     # #------------------------------------------------------------------------------------#
#     def test_play(self):
#         """Test Play Quiz """
#         print('...Play Quiz...')
#         res = self.client().post('/quizzes',  json={"previous_questions":[10, 11],
#                                                     "quiz_category":{"type":"Sports","id":"6"}})
#         data = json.loads(res.data)
#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(data['success'], True)
#
# # #------------------------------------------------------------------------------------#
# # # Search by question: Success
# # #------------------------------------------------------------------------------------#
# def test_search_by_question(self):
#     """Test Search question by question """
#     # print('...Search question for search term...')
#     res = self.client().post('/questions', json=self.new_question_for_search)
#     res = self.client().post('/questions/search', json={'searchTerm': self.search_question})
#     items = json.loads(res.data).get('questions', None)
#     self.assertEqual(res.status_code, 200)
#     self.assertTrue(items[0]['id'], True)
#
# # #------------------------------------------------------------------------------------#
# # # Search by category: Success
# # #------------------------------------------------------------------------------------#
# def test_search_by_category(self):
#     """Test Search question by category """
#     # print('...Search up question for selected category...')
#     # print('...Creating a new category...')
#     res = self.client().post('/categories', json=self.new_category)
#     items = json.loads(res.data).get('id', None)
#     # print('...Creating a new question for the newly created category...')
#     new_question_for_search = {
#         'question': 'Question for new category',
#         'answer': 'Unanswerable',
#         'category': items,
#         'difficulty': 1
#         }
#     res = self.client().post('/questions', json=new_question_for_search)
#
#     # print('...Searching for all questions linked to the new category...')
#     res = self.client().post('/categories/' + str(items) + '/questions')
#     data = json.loads(res.data)
#     self.assertEqual(res.status_code, 200)
#     self.assertEqual(data['totalQuestions'], 1)
#
# # #------------------------------------------------------------------------------------#
# # # Search by category: Failure
# # #------------------------------------------------------------------------------------#
# def test_search_by_category_404(self):
#     """Test Search question by category """
#     # print('...Search up question for selected category...')
#     res = self.client().post('/categories/' + str('1000') + '/questions')
#     data = json.loads(res.data)
#     self.assertEqual(res.status_code, 404)
#     self.assertEqual(data['success'], False)
#     self.assertEqual(data['message'], 'resource not found')
#
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
