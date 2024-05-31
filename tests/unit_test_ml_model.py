import unittest
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.impute import SimpleImputer

class TestSalaryModel(unittest.TestCase):
    def setUp(self):
        df = pd.read_csv('./data/data.csv')
        features = ['work_year', 'experience_level', 'employment_type', 'job_title', 'employee_residence', 'remote_ratio']
        X = df[features]
        y = df['salary_in_usd']
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        categorical_features = ['experience_level', 'employment_type', 'job_title', 'employee_residence']
        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])
        preprocessor = ColumnTransformer(
            transformers=[
                ('cat', categorical_transformer, categorical_features)
            ])
        self.model = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('regressor', LinearRegression())
        ])

    def test_model_performance(self):
        # validação cruzada com dados válidos
        mse_scores = cross_val_score(self.model, self.X_train, self.y_train, scoring='neg_mean_squared_error', cv=5)
        mse_mean = -mse_scores.mean()
        self.assertLessEqual(mse_mean, 3e9, "MSE is greater than acceptable threshold")

    def test_invalid_data(self):
        #  validação cruzada com dados inválidos
        invalid_data = pd.DataFrame({'work_year': [2023], 'experience_level': ['invalid'], 'employment_type': ['invalid'], 'job_title': ['invalid'], 'employee_residence': ['invalid'], 'remote_ratio': [100]})
        X_invalid = pd.concat([self.X_train, invalid_data], ignore_index=True)
        y_invalid = pd.concat([self.y_train, pd.Series([0])], ignore_index=True)  # Adicionando um valor de destino irrelevante
        try:
            mse_scores = cross_val_score(self.model, X_invalid, y_invalid, scoring='neg_mean_squared_error', cv=5)
            mse_mean = -mse_scores.mean()
            self.assertLessEqual(mse_mean, 3e9, "MSE is greater than acceptable threshold")
        except ValueError:
            pass  # ValueError quando dados inválidos são fornecidos

if __name__ == '__main__':
    unittest.main()
