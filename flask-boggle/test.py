from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!

   def setUp(self):
    self.client = app.test_client()
    app.config['TESTING'] = True 

   def test_home(self):
        with self.client:
            response = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))
            self.assertIn(b'<p>High Score:', response.data)
            self.assertIn(b'Score:', response.data)
            self.assertIn(b'Seconds Left:', response.data)
    
    def test_valid(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["L", "O", "G", "G", "G"], 
                                 ["L", "O", "G", "G", "G"], 
                                 ["L", "O", "G", "G", "G"], 
                                 ["L", "O", "G", "G", "G"], 
                                 ["L", "O", "G", "G", "G"]]
        response = self.client.get('/check-word?word=log')
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid(self):
        self.client.get('/')
        response = self.client.get('check-word?word=nothere')
        self.assertEqual(response.json['result'], 'not-on-board')
    
    def test_not_word(self):
        self.client.get('/')
        response = self.client.get('check-word?word=wtafewger')
        self.assertEqual(response.json['result'], 'not-word')
    

