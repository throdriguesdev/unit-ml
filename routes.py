from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from utils import home, predict, get_salary_data_from_api, display_graphs
import logging 
from flask import current_app
prediction_routes = Blueprint('prediction_routes', __name__)
@prediction_routes.route('/predict', methods=['POST'])
def prediction():
       try:
           current_app.logger.info('Submission received successfully')
           return predict(request)
    
       except Exception as e:
           current_app.logger.error('Error in prediction route: %s', str(e))

@prediction_routes.route('/ping')
def ping():
       try:
                return jsonify({'status': 'up'})
       except Exception as e:
                current_app.logger.error('Error ing ping route: %s',  str(e) )
                return jsonify({'error': 'An error occured'}), 500

    
@prediction_routes.route('/')
def index():
    return home()

@prediction_routes.route('/result', methods=['GET'])
def result():
    try:
        predicted_salary = float(request.args.get('predicted_salary'))
        job_title = request.args.get('job_title')
        employee_residence = request.args.get('employee_residence')
        if predicted_salary is None or job_title is None or employee_residence is None:
                        raise ValueError('Missing input data')
            

      
        api_data = get_salary_data_from_api(job_title, employee_residence)
        formatted_predicted_salary = f"${predicted_salary:,.0f}"

        return render_template('result.html', 
                               predicted_salary=formatted_predicted_salary, 
                               api_data=api_data)
    except ValueError as e:
        current_app.logger.error('Error in result route: %s', str(e) )
        return jsonify({'error': 'Invalid predicted salary provided'}), 400

@prediction_routes.route('/graphs', methods=['GET'])
def graphs():
    try:
        return display_graphs()
    except Exception as e:
        current_app.logger.error('Error in graphs route: %s', str(e))
        return jsonify({'error': 'An error occurred'}), 500

@prediction_routes.route('/report', methods=['GET'])
def report():
    try: 
        return render_template('report.html')
    except Exception as e:
        current_app.logger.error('Error in predictions route: %s', str(e))
        return jsonify({'error': 'An error occurred'}), 500

