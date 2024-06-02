import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, median_absolute_error
from sklearn.impute import SimpleImputer
from joblib import dump

# Carregar os dados
df = pd.read_csv('data/data.csv')

# Definir features e target
features = ['experience_level', 'employment_type', 'job_title', 'employee_residence']
X = df[features]
y = df['salary_in_usd']

# Dividir os dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Definir transformações para variáveis categóricas e numéricas
categorical_features = ['experience_level', 'employment_type', 'job_title', 'employee_residence']

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Aplicar transformações
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', categorical_transformer, categorical_features)
    ])

# Criar pipeline com diferentes regressores
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor())
])

# Definir parâmetros para Grid Search incluindo diferentes modelos e seus hiperparâmetros
param_grid = [
    {
        'regressor': [RandomForestRegressor()],
        'regressor__n_estimators': [100, 200, 300],
        'regressor__max_depth': [10, 20, 30],
        'regressor__min_samples_split': [2, 5, 10]
    },
    {
        'regressor': [GradientBoostingRegressor()],
        'regressor__n_estimators': [100, 200, 300],
        'regressor__learning_rate': [0.01, 0.1, 0.2],
        'regressor__max_depth': [3, 4, 5]
    },
    {
        'regressor': [AdaBoostRegressor()],
        'regressor__n_estimators': [50, 100, 200],
        'regressor__learning_rate': [0.01, 0.1, 1.0]
    }
]

# Realizar Grid Search
grid_search = GridSearchCV(model, param_grid, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)
grid_search.fit(X_train, y_train)

# Obter melhores parâmetros
best_params = grid_search.best_params_
print(f'Melhores parâmetros: {best_params}')

# Treinar modelo com melhores parâmetros
best_model = grid_search.best_estimator_
predictions = best_model.predict(X_test)

# Avaliar o modelo otimizado
mse = mean_squared_error(y_test, predictions)
r2 = r2_score(y_test, predictions)
mae = mean_absolute_error(y_test, predictions)
medae = median_absolute_error(y_test, predictions)
print(f'MSE: {mse}')
print(f'R^2: {r2}')
print(f'MAE: {mae}')
print(f'MedAE: {medae}')

# Salvar o melhor modelo
dump(best_model, 'ml/best_salary_model2.joblib')
