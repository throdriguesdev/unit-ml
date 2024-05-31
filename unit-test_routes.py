import unittest
import os
import sys
from flask import Flask
# Adiciona o diretório raiz do projeto ao caminho do sistema Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Agora podemos importar o módulo routes
from routes import prediction_routes  

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(prediction_routes)
        self.client = self.app.test_client()

    def test_ping_route(self):
        response = self.client.get('/ping')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'up'})

    def test_index_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Previsor de Sal\xc3\xa1rio', response.data)  


    def test_result_route(self):
        # Simula a chamada à rota /result com os parâmetros necessários
        response = self.client.get('/result?predicted_salary=50000&job_title=Data%20Analyst&employee_residence=US')
        self.assertEqual(response.status_code, 200)  # Verifica se a resposta tem o código 200
        self.assertIn(b'$50,000', response.data)  # Verifica se o salário previsto está presente na resposta

if __name__ == '__main__':
    unittest.main()
