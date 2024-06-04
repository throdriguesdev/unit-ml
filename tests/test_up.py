### TESTE UNITARIO API UP 


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
# Teste de Verificação do Status com Ping:
# - Objetivo: Este teste verifica se a rota /ping está respondendo corretamente e retornando o status “up”.
# - Implementação:
# - O teste configura a aplicação Flask em modo de teste e cria um cliente de teste para a mesma.
# - Em seguida, ele faz uma solicitação GET para a rota /ping e verifica o código de status da resposta.
# - O teste confirma se o status da resposta é 200, indicando que a rota está acessível e operante.
# - Além disso, ele verifica se a resposta JSON contém o valor 'up' para o status, garantindo o funcionamento adequado da rota.


if __name__ == '__main__':
    unittest.main()
