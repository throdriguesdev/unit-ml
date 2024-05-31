from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from utils import home, predict, get_salary_data_from_api, get_data, display_data, display_graphs

prediction_routes = Blueprint('prediction_routes', __name__)

@prediction_routes.route('/predict', methods=['POST'])
def prediction():
    return predict(request)

@prediction_routes.route('/ping')
def ping():
    return jsonify({'status': 'up'})

@prediction_routes.route('/')
def index():
    return home()

@prediction_routes.route('/result', methods=['GET'])
def result():
    try:
        predicted_salary = float(request.args.get('predicted_salary'))
        job_title = request.args.get('job_title')
        employee_residence = request.args.get('employee_residence')

        # Chamada da API para obter dados salariais
        api_data = get_salary_data_from_api(job_title, employee_residence)
        
        # Formatação do salário previsto
        formatted_predicted_salary = f"${predicted_salary:,.0f}"

        return render_template('result.html', 
                               predicted_salary=formatted_predicted_salary, 
                               api_data=api_data)
    except ValueError:
        return jsonify({'error': 'Invalid predicted salary provided'}), 400

@prediction_routes.route('/data', methods=['GET'])
def data():
    return display_data()

@prediction_routes.route('/graphs', methods=['GET'])
def graphs():
    return display_graphs()
