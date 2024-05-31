import unittest
from unittest.mock import MagicMock, patch
from flask import Flask
from flask.testing import FlaskClient
from routes import prediction_routes

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(prediction_routes)
        self.client = self.app.test_client()

    

    def test_predict_route_invalid_data(self):
        # Testar rota /predict com dados inválidos
        response = self.client.post('/predict', json={'invalid_data': 'invalid'})  # Enviar dados inválidos
        self.assertEqual(response.status_code, 400)  # Espera-se um código de status 400


    def test_result_route_invalid_prediction(self):
        # Testar rota /result com previsão inválida
        response = self.client.get('/result?predicted_salary=invalid&job_title=Data%20Analyst&employee_residence=US')
        self.assertEqual(response.status_code, 400)  # Espera-se um código de status 400

if __name__ == '__main__':
    unittest.main()
