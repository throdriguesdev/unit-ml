import pandas as pd
from joblib import load
from flask import current_app, render_template, request, jsonify
import numpy as np
from flask import redirect, url_for


loaded_model = load('ml/salary_model.joblib')
data = pd.read_csv('data/data.csv')


experience_levels = data['experience_level'].unique().tolist()
employment_types = data['employment_type'].unique().tolist()
employee_residences = data['employee_residence'].unique().tolist()
job_titles = data['job_title'].unique().tolist()

def calculate_mean_salary(data, job_titles):
    if isinstance(data, pd.DataFrame):
        selected_titles = data[data['job_title'].isin(job_titles)]
        mean_salary = selected_titles['salary_in_usd'].mean()
        return mean_salary
    else:
        return None

def home():
    return render_template('index.html', 
                           experience_levels=experience_levels,
                           employment_types=employment_types,
                           employee_residences=employee_residences,
                           job_titles=job_titles)

def get_data():
    return jsonify({
        'experience_levels': experience_levels,
        'employment_types': employment_types,
        'employee_residences': employee_residences,
        'job_titles': job_titles
    })

def predict(request):

    data = request.get_json()


    experience_level = data['experience_level']
    employment_type = data['employment_type']
    job_title = data['job_title']
    employee_residence = data['employee_residence']
    remote_ratio = float(data['remote_ratio'])


    mean_salary = calculate_mean_salary(data, job_title)


    user_input = pd.DataFrame({
        'experience_level': [experience_level],
        'employment_type': [employment_type],
        'job_title': [job_title],
        'employee_residence': [employee_residence],
        'remote_ratio': [remote_ratio]
    })

    predicted_salary = loaded_model.predict(user_input)

    predicted_salary_str = str(predicted_salary[0])


    return predicted_salary_str


