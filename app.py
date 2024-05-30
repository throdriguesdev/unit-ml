from flask import Flask, request, jsonify, render_template
import pandas as pd
from joblib import load
app = Flask(__name__)
loaded_model = load('ml/salary_model.joblib')
data = pd.read_csv('data/data.csv')
job_titles = data['job_title'].unique()
@app.route('/')
def home():
    return render_template('index.html', job_titles=job_titles)
@app.route('/predict', methods=['POST'])
def predict():
    experience_level = request.form['experience_level']
    employment_type = request.form['employment_type']
    job_title = request.form['job_title']
    employee_residence = request.form['employee_residence']
    remote_ratio = float(request.form['remote_ratio'])
    user_input = pd.DataFrame({
        'experience_level': [experience_level],
        'employment_type': [employment_type],
        'job_title': [job_title],
        'employee_residence': [employee_residence],
        'remote_ratio': [remote_ratio]
    })
    predicted_salary = loaded_model.predict(user_input)
    return render_template('result.html', predicted_salary=predicted_salary[0])

if __name__ == '__main__':
    app.run(debug=True)
