import unittest
import pandas as pd
from joblib import load

class TestSalaryPrediction(unittest.TestCase):
    def test_valid_prediction(self):
        loaded_model = load('./ml/salary_model.joblib')

        user_input = pd.DataFrame({
            'experience_level': ['SE'],  
            'employment_type': ['FT'],  
            'job_title': ['Data Analyst'], 
            'employee_residence': ['US'],  
            'remote_ratio': [100],  
        })
        predicted_salary = loaded_model.predict(user_input)

    
        self.assertIsInstance(predicted_salary[0], float, "A previsão não é um valor numérico")
        self.assertGreaterEqual(predicted_salary[0], 0, "A previsão é menor que zero")
        self.assertLessEqual(predicted_salary[0], 1e6, "A previsão é maior que 1,000,000 USD")

if __name__ == '__main__':
    unittest.main()
