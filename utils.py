import pandas as pd
from joblib import load
from flask import  render_template
from flask import current_app, render_template
loaded_model = load('ml/salary_model.joblib')
data = pd.read_csv('data/data.csv')
experience_levels = data['experience_level'].unique()
employment_types = data['employment_type'].unique()
employee_residences = data['employee_residence'].unique()
job_titles = data['job_title'].unique()
def calculate_mean_salary(data, job_titles):
    if isinstance(data, pd.DataFrame):
        selected_titles = data[data['job_title'].isin(job_titles)]
        mean_salary = selected_titles['salary_in_usd'].mean()
        return mean_salary
    else:
        return None  #
def home():
    with current_app.app_context():
        return render_template('index.html', experience_levels=experience_levels,
                               employment_types=employment_types, employee_residences=employee_residences,
                               job_titles=job_titles)
def predict(request):
    experience_level = request.form['experience_level']
    employment_type = request.form['employment_type']
    job_title = request.form.getlist('job_title')
    employee_residence = request.form['employee_residence']
    remote_ratio = float(request.form['remote_ratio'])
    mean_salary = calculate_mean_salary(data, job_title)
    user_input = pd.DataFrame({
        'experience_level': [experience_level],
        'employment_type': [employment_type],
        'job_title': [', '.join(job_title)],
        'employee_residence': [employee_residence],
        'remote_ratio': [remote_ratio]
    })
    predicted_salary = loaded_model.predict(user_input)
    return render_template('result.html', predicted_salary=predicted_salary[0], mean_salary=mean_salary)
