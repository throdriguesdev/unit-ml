import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

class TestPing(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_ping(self):
        response = self.app.get('/ping')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'up'})

if __name__ == '__main__':
    unittest.main()
