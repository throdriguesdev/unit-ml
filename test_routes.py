#TESTA AS PRINCIPAIS ROTAS
import unittest
import os
import sys
from flask import Flask
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
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
        
        #    Teste da Rota de Ping:
# - Objetivo: Este teste verifica se a rota de /ping está respondendo corretamente e retornando o status “up”.
# - Implementação:Teste de Verificação do Status com Ping:
# - Objetivo: Este teste verifica se a rota /ping está respondendo corretamente e retornando o status “up”.
# - Implementação:
# - O teste configura a aplicação Flask em modo de teste e cria um cliente de teste para a mesma.
# - Em seguida, ele faz uma solicitação GET para a rota /ping e verifica o código de status da resposta.
# - O teste confirma se o status da resposta é 200, indicando que a rota está acessível e operante.
# - Além disso, ele verifica se a resposta JSON contém o valor 'up' para o status, garantindo o funcionamento adequado da rota.ta JSON contém o status 'up', garantindo que a rota esteja funcionando conforme o esperado.
# - Resultado Esperado:
# - Ao executar o teste com sucesso, ele confirma que a rota /ping está operacional e retorna o status “up”.
          
    def test_index_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Previsor de Sal\xc3\xa1rio', response.data)  
# Teste da Rota de Índice:
# - Objetivo: Este teste valida a resposta e o conteúdo da rota raiz (/) da aplicação.
# - Implementação:
# - O teste envia uma solicitação GET para a rota raiz e verifica se o código de status da resposta é 200.
# - Ele verifica se a resposta contém a string 'Previsor de Salário', confirmando que a página inicial está sendo renderizada corretamente.
# - Resultado Esperado:
# - Ao passar no teste, ele assegura que a página inicial está sendo exibida corretamente com o texto esperado.
    def test_result_route(self):
        response = self.client.get('/result?predicted_salary=50000&job_title=Data%20Analyst&employee_residence=US')
        self.assertEqual(response.status_code, 200)  # Verifica se a resposta tem o código 200
        self.assertIn(b'$50,000', response.data)  # Verifica se o salário previsto está presente na resposta
#         Teste da Rota de Resultado:
# - Objetivo: Este teste verifica a funcionalidade da rota /result ao passar parâmetros de previsão de salário.
# - Implementação:
# - O teste faz uma solicitação GET para a rota /result com parâmetros simulados de previsão de salário.
# - Ele verifica se o código de status da resposta é 200, indicando uma resposta bem-sucedida.
# - Além disso, o teste confirma se a resposta contém a string '$50,000', garantindo que o valor de salário previsto está presente na resposta.
# - Resultado Esperado:
# - Ao ser executado com sucesso, o teste valida que a rota /result está processando corretamente os parâmetros de previsão de salário e exibindo o resultado esperado.
if __name__ == '__main__':
    unittest.main()
