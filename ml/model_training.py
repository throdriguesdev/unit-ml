import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.impute import SimpleImputer
from joblib import dump

# Carregar os dados
df = pd.read_csv('data/data.csv')

# Definir as features, removendo 'company_size' e 'company_location'
features = ['work_year', 'experience_level', 'employment_type', 'job_title', 'employee_residence', 'remote_ratio']

# Selecionar features e target
X = df[features]
y = df['salary_in_usd']

# Dividir os dados em conjunto de treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Definir as features categóricas
categorical_features = ['experience_level', 'employment_type', 'job_title', 'employee_residence']

# Pré-processamento para as features categóricas
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Combinar pré-processamento
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', categorical_transformer, categorical_features)
    ])

# Criar pipeline com pré-processamento e modelo de regressão linear
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', LinearRegression())
])

# Treinar o modelo
model.fit(X_train, y_train)

# Fazer previsões
predictions = model.predict(X_test)

# Avaliar o modelo
mse = mean_squared_error(y_test, predictions)
r2 = r2_score(y_test, predictions)
print(f'MSE: {mse}')
print(f'R^2: {r2}')

# Salvar o modelo treinado
dump(model, 'ml/salary_model.joblib')
