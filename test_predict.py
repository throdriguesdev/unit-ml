# Teste de Predição Válida:
# - Objetivo: Este teste valida a funcionalidade de predição do  modelo de salário ao usar dados de entrada corretos.
# - Implementação:
# - O teste carrega o modelo de salário previamente treinado usando o joblib.
# - Em seguida, ele cria um DataFrame do Pandas contendo dados de entrada válidos, como nível de experiência, tipo de emprego, título do cargo, residência do funcionário e taxa de trabalho remoto.
# - O modelo é então usado para prever o salário com base nos dados de entrada fornecidos.
# - O teste verifica se a previsão retornada é do tipo float, garantindo que seja um valor numérico.
# - Além disso, ele verifica se a previsão está dentro do intervalo esperado, ou seja, maior ou igual a 0 e menor ou igual a 1.000.000 de dólares.
##TESTE EXECUTADO DE FORMA AUTOMATIZADA AO RODAR O PYTEST
import pandas as pd
from joblib import load
def test_valid_prediction():
    loaded_model = load('./ml/salary_model.joblib')

    user_input = pd.DataFrame({
        'experience_level': ['SE'],
        'employment_type': ['FT'],
        'job_title': ['Data Analyst'],
        'employee_residence': ['US'],
        'remote_ratio': [100],
    })
    predicted_salary = loaded_model.predict(user_input)

    assert isinstance(predicted_salary[0], float), "A previsão não é um valor numérico"

    assert predicted_salary[0] >= 0, "A previsão é menor que zero"
    assert predicted_salary[0] <= 1e6, "A previsão é maior que 1,000,000 USD"
