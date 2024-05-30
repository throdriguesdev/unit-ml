import unittest
import pandas as pd
import numpy as np
from joblib import load
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

class TestSalaryModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Carregar o modelo salvo
        cls.model = load('salary_model.joblib')

    def test_model_instance(self):
        # Testar se o modelo é uma instância de Pipeline
        self.assertIsInstance(self.model, Pipeline, "Model is not a Pipeline instance")

    def test_prediction_output(self):
        # Testar se a previsão é um número
        user_input = pd.DataFrame({
            'work_year': [2023],
            'experience_level': ['SE'],
            'employment_type': ['FT'],
            'job_title': ['Principal Data Scientist'],
            'employee_residence': ['ES'],
            'remote_ratio': [100]
        })
        prediction = self.model.predict(user_input)
        self.assertIsInstance(prediction[0], np.float64, "Prediction is not a float")

    def test_reasonable_prediction_range(self):
        # Testar se a previsão está dentro de um intervalo razoável
        user_input = pd.DataFrame({
            'work_year': [2023],
            'experience_level': ['SE'],
            'employment_type': ['FT'],
            'job_title': ['Principal Data Scientist'],
            'employee_residence': ['ES'],
            'remote_ratio': [100]
        })
        prediction = self.model.predict(user_input)
        self.assertGreaterEqual(prediction[0], 0, "Prediction is less than 0")
        self.assertLessEqual(prediction[0], 1e6, "Prediction is greater than 1,000,000")

    def test_multiple_predictions(self):
        # Testar o modelo com múltiplas entradas
        user_inputs = pd.DataFrame({
            'work_year': [2023, 2023],
            'experience_level': ['SE', 'MI'],
            'employment_type': ['FT', 'CT'],
            'job_title': ['Principal Data Scientist', 'ML Engineer'],
            'employee_residence': ['ES', 'US'],
            'remote_ratio': [100, 50]
        })
        predictions = self.model.predict(user_inputs)
        self.assertEqual(len(predictions), 2, "Number of predictions does not match number of inputs")

    def test_invalid_data(self):
        # Testar o comportamento do modelo com dados inválidos
        invalid_input = pd.DataFrame({
            'work_year': [2023],
            'experience_level': [None],  # Nível de experiência faltando
            'employment_type': ['FT'],
            'job_title': ['Principal Data Scientist'],
            'employee_residence': ['ES'],
            'remote_ratio': [100]
        })
        try:
            prediction = self.model.predict(invalid_input)
            self.assertIsInstance(prediction[0], np.float64, "Prediction is not a float for invalid input")
        except ValueError as e:
            self.fail(f"Model raised ValueError unexpectedly: {str(e)}")

    def test_model_performance(self):
        # Carregar os dados de teste
        df = pd.read_csv('data.csv')
        features = ['work_year', 'experience_level', 'employment_type', 'job_title', 'employee_residence', 'remote_ratio']
        X = df[features]
        y = df['salary_in_usd']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Fazer previsões
        predictions = self.model.predict(X_test)
        
        # Calcular métricas de desempenho
        mse = mean_squared_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)
        
        # Testar se o MSE está dentro de um limite aceitável
        self.assertLessEqual(mse, 1e9, "MSE is greater than acceptable threshold")

        
        # Testar se o R^2 é razoável
        self.assertLessEqual(mse, 2e9, "MSE is greater than acceptable threshold")


if __name__ == '__main__':
    unittest.main()
