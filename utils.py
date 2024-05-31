import pandas as pd
from joblib import load
from flask import current_app, render_template, request, jsonify, redirect, url_for
import numpy as np
import requests

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

def get_salary_data_from_api(job_title, location):
    url = "https://job-salary-data.p.rapidapi.com/job-salary"
    querystring = {"job_title": job_title, "location": location, "radius": "200"}
    headers = {
        "X-RapidAPI-Key": "2d562a2038msh442eec8c1d9f5a7p1049a4jsn6954b73a715c",
        "X-RapidAPI-Host": "job-salary-data.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "OK":
            return data["data"]
    return []


def predict(request):
    data = request.get_json()
    if data is None or 'experience_level' not in data:
        return jsonify({'error': 'Invalid data: experience_level is missing'}), 400

    experience_level = data['experience_level']
    employment_type = data['employment_type']
    job_title = data['job_title']
    employee_residence = data['employee_residence']
    remote_ratio = float(data.get('remote_ratio', 100))  # Default to 100% if not provided

    user_input = pd.DataFrame({
        'experience_level': [experience_level],
        'employment_type': [employment_type],
        'job_title': [job_title],
        'employee_residence': [employee_residence],
        'remote_ratio': [remote_ratio]
    })

    predicted_salary = loaded_model.predict(user_input)[0]
    predicted_salary_str = str(predicted_salary)

    return redirect(url_for('prediction_routes.result', predicted_salary=predicted_salary_str, job_title=job_title, employee_residence=employee_residence))
